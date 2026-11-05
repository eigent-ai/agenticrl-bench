"""Gateway in front of the team's rollout engine (SGLang 0.5.9 on 127.0.0.1:31000, key-protected).

The rollout side gets SGLang's native ``/generate`` and ``/abort_request`` (plus ``/health``), nothing else. Every
generation gets an engine request id of its own; a caller's ``rid`` keeps working for ``/abort_request`` and comes
back in ``meta_info.id``. When the caller hangs up, its generation is aborted. Inside a live job the gateway also
keeps a record of every generation and of the trainer's weight updates.

    python3 -I gateway.py --port 30000          # the box's shared gateway (no records)
"""
import argparse
import asyncio
import json
import time
import uuid

import aiohttp
from aiohttp import web

ENGINE_URL = "http://127.0.0.1:31000"
KEY_FILE = "/var/lib/agentrl-live/engine.key"
DEFAULT_MAX_NEW_TOKENS = 128  # SGLang's default when sampling_params has none


def _err(status: int, message: str) -> web.Response:
    return web.json_response({"error": message}, status=status)


class Gateway:
    def __init__(self, engine_url: str = ENGINE_URL, key: str | None = None, record: bool = False):
        self.engine_url = engine_url.rstrip("/")
        if key is None:
            with open(KEY_FILE) as f:
                key = f.read().strip()
        self.headers = {"Authorization": f"Bearer {key}"}
        self.record = record
        self.log: list[dict] = []        # finished generations (record mode)
        self.refused: list[dict] = []    # calls the engine refused (non-200), record mode
        self.updates: list[dict] = []    # weight updates issued by the job's trainer: {"id", "u0", "u1"}
        self.failures: list[dict] = []   # calls the engine could not be reached for (box-side)
        self.inflight: dict[str, dict] = {}
        self.by_caller: dict[str, set] = {}
        self.prefix = uuid.uuid4().hex[:10]
        self.seq = 0
        self.http: aiohttp.ClientSession | None = None

    async def session(self) -> aiohttp.ClientSession:
        if self.http is None or self.http.closed:
            # one connection per call: a pooled keep-alive connection the engine closed meanwhile would fail the call
            self.http = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=3600),
                                              connector=aiohttp.TCPConnector(limit=0, force_close=True))
        return self.http

    async def close(self):
        if self.http is not None:
            await self.http.close()

    async def engine_post(self, path: str, payload: dict, timeout: float | None = None) -> tuple[int, str]:
        http = await self.session()
        kw = {"timeout": aiohttp.ClientTimeout(total=timeout)} if timeout else {}
        async with http.post(self.engine_url + path, json=payload, headers=self.headers, **kw) as r:
            return r.status, await r.text()

    async def _abort(self, rid: str):
        try:
            await self.engine_post("/abort_request", {"rid": rid}, timeout=30)
        except Exception:
            pass

    # --- HTTP ------------------------------------------------------------------------------------------------------
    async def generate(self, request: web.Request) -> web.Response:
        t0 = time.time()
        try:
            body = await request.json()
        except Exception:
            return _err(400, "request body is not JSON")
        if not isinstance(body, dict):
            return _err(400, "request body must be a JSON object")
        ids = body.get("input_ids")
        if not isinstance(ids, list) or not ids or not all(type(x) is int for x in ids):
            return _err(400, "input_ids required (one flat list of token ids)")
        if body.get("text") is not None or body.get("input_embeds") is not None:
            return _err(400, "send input_ids only")
        if body.get("stream"):
            return _err(400, "streaming is not served here")
        sp = body.get("sampling_params") or {}
        if not isinstance(sp, dict):
            return _err(400, "sampling_params must be an object")
        caller = body.get("rid")
        caller = None if caller is None else str(caller)
        self.seq += 1
        rid = f"{self.prefix}-{self.seq:09d}"
        fwd = dict(body, rid=rid, return_logprob=True, stream=False)
        st = {"rid": rid, "engine_rid": f"{rid}.0", "caller": caller, "t0": t0, "caller_abort": False, "gone": False}
        self.inflight[rid] = st
        if caller is not None:
            self.by_caller.setdefault(caller, set()).add(rid)
        async def call():
            for attempt in range(3):  # the engine never got the call if the connection failed: try again
                try:
                    st["engine_rid"] = f"{rid}.{attempt}"  # a fresh engine rid per attempt
                    return await self.engine_post("/generate", dict(fwd, rid=st["engine_rid"]))
                except aiohttp.ClientConnectionError:
                    if attempt == 2 or st["gone"] or st["caller_abort"]:
                        raise
                    await asyncio.sleep(0.5)

        task = asyncio.ensure_future(call())
        try:
            while not task.done():
                await asyncio.wait({task}, timeout=0.05)
                if not task.done() and not st["gone"]:
                    tr = request.transport
                    if tr is None or tr.is_closing():  # the caller hung up: nobody will get this generation
                        st["gone"] = True
                        await self._abort(st["engine_rid"])
            status, text = task.result()
        except Exception as e:
            self.failures.append({"t": time.time(), "rid": caller or rid, "error": f"{type(e).__name__}: {e}"[:300]})
            return _err(502, f"engine unreachable: {type(e).__name__}: {e}")
        finally:
            self.inflight.pop(rid, None)
            if caller is not None:
                s = self.by_caller.get(caller)
                if s is not None:
                    s.discard(rid)
                    if not s:
                        self.by_caller.pop(caller, None)
        t1 = time.time()
        if status != 200:
            if self.record:
                self.refused.append({"t0": t0, "t1": t1, "rid": caller or rid, "status": status,
                                     "n_input": len(ids), "error": text[:2000]})
            return web.Response(status=status, text=text, content_type="application/json")
        try:
            out = json.loads(text)
            meta = out["meta_info"]
            pairs = meta.get("output_token_logprobs") or []
            out_ids = [int(p[1]) for p in pairs]
            lps = [float(p[0]) for p in pairs]
        except Exception as e:
            return _err(502, f"unreadable engine response: {type(e).__name__}: {e}")
        fr = meta.get("finish_reason")
        ftype = fr.get("type") if isinstance(fr, dict) else None
        finish = ftype if ftype in ("stop", "length", "abort") else "stop"
        ended = "complete"
        if finish == "abort":
            if st["caller_abort"]:
                ended = "abort_request"
            elif st["gone"]:
                ended = "client_disconnected"
            elif any(t0 <= u["u0"] <= t1 for u in self.updates):
                ended = "injected_abort"  # weights were updated under it
            else:
                ended = "engine_abort"
        if self.record:
            mx = sp.get("max_new_tokens")
            self.log.append({"t0": t0, "t1": t1, "rid": caller if caller is not None else rid, "input_ids": ids,
                             "output_ids": out_ids, "log_probs": lps, "finish": finish, "ended": ended,
                             "max_new_tokens": int(mx) if mx is not None else DEFAULT_MAX_NEW_TOKENS,
                             "weight_version": meta.get("weight_version")})
        if caller is not None:
            meta["id"] = caller
        return web.json_response(out)

    async def abort_request(self, request: web.Request) -> web.Response:
        try:
            body = await request.json()
        except Exception:
            body = {}
        caller = body.get("rid") if isinstance(body, dict) else None
        if caller is not None:
            for rid in list(self.by_caller.get(str(caller), ())):
                st = self.inflight.get(rid)
                if st is not None:
                    st["caller_abort"] = True
                    await self._abort(st["engine_rid"])
        return web.json_response({"ok": True})

    async def health(self, request: web.Request) -> web.Response:
        try:
            http = await self.session()
            async with http.get(self.engine_url + "/health", timeout=aiohttp.ClientTimeout(total=10)) as r:
                ok = r.status == 200
        except Exception:
            ok = False
        return web.json_response({"status": "ok" if ok else "unavailable"}, status=200 if ok else 503)

    def app(self) -> web.Application:
        app = web.Application(client_max_size=512 * 1024 * 1024)
        app.router.add_post("/generate", self.generate)
        app.router.add_post("/abort_request", self.abort_request)
        app.router.add_get("/health", self.health)
        app.router.add_get("/health_generate", self.health)
        return app


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=30000)
    args = ap.parse_args()
    gw = Gateway()
    app = gw.app()

    async def _close(_app):
        await gw.close()

    app.on_cleanup.append(_close)
    web.run_app(app, host=args.host, port=args.port, access_log=None, print=None)


if __name__ == "__main__":
    main()
