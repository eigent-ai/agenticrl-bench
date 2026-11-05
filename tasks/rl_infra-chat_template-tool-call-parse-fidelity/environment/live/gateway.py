"""/generate front of the live engine (runs as root, started by /opt/live/run.sh).

    python3 -I gateway.py --listen-port 30000 --engine-port 31000 --auth-file F                     (dev endpoint)
    python3 -I gateway.py --listen-port 0 --port-file P --engine-port 31000 --auth-file F --log L    (one live batch)

Only POST /generate (token ids in, token ids + logprobs out, SGLang's native schema) and GET /health are served; the
engine itself is not reachable without its key. In batch mode the sampling parameters are the launcher's rollout
settings (temperature 1, top-p 1, response <= 2048 tokens, context <= 16384, special tokens kept, stop token kept) and
every request is appended to the batch log.
"""
import argparse
import asyncio
import json
import time

from aiohttp import ClientConnectionError, ClientSession, ClientTimeout, TCPConnector, web

VOCAB = 248320  # Qwen3.5-2B embedding rows
MAX_ENGINE_CTX = 32768
BATCH_RESPONSE_LEN, BATCH_CONTEXT_LEN = 2048, 16384
DEV_SAMPLING_KEYS = {
    "temperature", "top_p", "top_k", "min_p", "max_new_tokens", "min_new_tokens", "stop", "stop_token_ids",
    "skip_special_tokens", "spaces_between_special_tokens", "no_stop_trim", "ignore_eos", "repetition_penalty",
    "frequency_penalty", "presence_penalty", "sampling_seed",
}
NOT_SERVED = {"text", "input_embeds", "image_data", "video_data", "audio_data", "lora_path", "stream", "session_params",
              "bootstrap_host", "custom_logit_processor", "return_hidden_states"}


class Gateway:
    def __init__(self, a):
        self.a = a
        self.batch = a.log is not None
        self.auth = {"Authorization": "Bearer " + open(a.auth_file).read().strip()}
        self.url = f"http://127.0.0.1:{a.engine_port}"
        self.seq = 0
        self.log = open(a.log, "a", buffering=1) if self.batch else None
        self.session = None

    async def start(self, app):
        self.session = ClientSession(connector=TCPConnector(limit=2048), timeout=ClientTimeout(total=None))

    async def stop(self, app):
        await self.session.close()
        if self.log:
            self.log.close()

    def _write(self, rec):
        if self.log:
            self.log.write(json.dumps(rec, separators=(",", ":")) + "\n")

    def _reject(self, seq, t0, reason, n_in=None):
        self._write({"seq": seq, "t0": t0, "status": 400, "reason": reason, "input_len": n_in})
        return web.json_response({"error": reason}, status=400)

    async def health(self, request):
        try:
            async with self.session.get(self.url + "/health", timeout=ClientTimeout(total=10)) as r:
                return web.Response(status=r.status, text="ok" if r.status == 200 else "engine not ready")
        except Exception:  # noqa: BLE001
            return web.Response(status=503, text="engine not ready")

    async def generate(self, request):
        self.seq += 1
        seq, t0 = self.seq, time.time()
        try:
            body = await request.json()
        except Exception:  # noqa: BLE001
            return self._reject(seq, t0, "body is not JSON")
        if not isinstance(body, dict):
            return self._reject(seq, t0, "body is not an object")
        ids = body.get("input_ids")
        if not (isinstance(ids, list) and ids and all(type(x) is int and 0 <= x < VOCAB for x in ids)):
            return self._reject(seq, t0, "input_ids must be a non-empty list of token ids")
        if len(ids) >= MAX_ENGINE_CTX:
            return self._reject(seq, t0, "input too long", len(ids))
        bad = sorted(k for k in NOT_SERVED if body.get(k) not in (None, False))
        if bad:
            return self._reject(seq, t0, f"not served here: {bad}", len(ids))
        sp = body.get("sampling_params") or {}
        if not isinstance(sp, dict):
            return self._reject(seq, t0, "sampling_params must be an object", len(ids))
        if self.batch:
            max_new = min(BATCH_RESPONSE_LEN, BATCH_CONTEXT_LEN - len(ids))
            if max_new <= 0:
                return self._reject(seq, t0, "context full", len(ids))
            fsp = {"temperature": 1.0, "top_p": 1.0, "top_k": -1, "max_new_tokens": max_new,
                   "skip_special_tokens": False, "no_stop_trim": True, "spaces_between_special_tokens": False}
            fwd = {"input_ids": ids, "sampling_params": fsp, "return_logprob": True}
        else:
            fsp = {k: v for k, v in sp.items() if k in DEV_SAMPLING_KEYS}
            mnt = fsp.get("max_new_tokens", 128)
            if type(mnt) is not int or mnt < 0:
                return self._reject(seq, t0, "max_new_tokens must be a non-negative int", len(ids))
            fsp["max_new_tokens"] = min(mnt, MAX_ENGINE_CTX - len(ids))
            fwd = {"input_ids": ids, "sampling_params": fsp, "return_logprob": bool(body.get("return_logprob", False))}
            tln = body.get("top_logprobs_num")
            if type(tln) is int and 0 < tln <= 20:
                fwd["top_logprobs_num"] = tln
        for attempt in range(4):  # a pooled connection the engine already closed fails before any answer: resend
            try:
                async with self.session.post(self.url + "/generate", json=fwd, headers=self.auth) as r:
                    status, payload = r.status, await r.read()
                break
            except ClientConnectionError as e:
                status, payload = 502, json.dumps({"error": f"engine unreachable: {type(e).__name__}"}).encode()
                await asyncio.sleep(0.2 * (attempt + 1))
            except Exception as e:  # noqa: BLE001
                status, payload = 502, json.dumps({"error": f"engine unreachable: {type(e).__name__}"}).encode()
                break
        t1 = time.time()
        if self.batch:
            rec = {"seq": seq, "t0": t0, "t1": t1, "status": status, "input_ids": ids, "requested": sp}
            if status == 200:
                try:
                    out = json.loads(payload)
                    mi = out["meta_info"]
                    lp = mi.get("output_token_logprobs") or []
                    rec.update({"text": out["text"], "output_ids": [int(x[1]) for x in lp],
                                "logprobs": [float(x[0]) for x in lp], "finish_reason": mi.get("finish_reason"),
                                "prompt_tokens": mi.get("prompt_tokens"), "completion_tokens": mi.get("completion_tokens"),
                                "cached_tokens": mi.get("cached_tokens")})
                except Exception as e:  # noqa: BLE001
                    rec.update({"status": 502, "error": f"unreadable engine answer: {type(e).__name__}"})
                    status = 502
                    payload = json.dumps({"error": "unreadable engine answer"}).encode()
            else:
                rec["error"] = payload[:500].decode(errors="replace")
            self._write(rec)
        return web.Response(status=status, body=payload, content_type="application/json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--listen-port", type=int, required=True)
    ap.add_argument("--port-file", default=None)
    ap.add_argument("--engine-port", type=int, required=True)
    ap.add_argument("--auth-file", required=True)
    ap.add_argument("--log", default=None)
    a = ap.parse_args()
    gw = Gateway(a)
    app = web.Application(client_max_size=64 * 1024 * 1024)
    app.on_startup.append(gw.start)
    app.on_cleanup.append(gw.stop)
    app.router.add_post("/generate", gw.generate)
    app.router.add_get("/health", gw.health)

    async def serve():
        runner = web.AppRunner(app, access_log=None)
        await runner.setup()
        site = web.TCPSite(runner, "127.0.0.1", a.listen_port, backlog=2048)
        await site.start()
        port = site._server.sockets[0].getsockname()[1]
        if a.port_file:
            with open(a.port_file + ".tmp", "w") as f:
                f.write(str(port))
            import os
            os.replace(a.port_file + ".tmp", a.port_file)
        stop = asyncio.Event()
        import signal
        loop = asyncio.get_running_loop()
        for s in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(s, stop.set)
        await stop.wait()
        await runner.cleanup()

    asyncio.run(serve())


if __name__ == "__main__":
    main()
