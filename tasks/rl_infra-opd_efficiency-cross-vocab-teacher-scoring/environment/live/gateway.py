"""Scoring gateway in front of the teacher engine (root service of the box).

The engine (SGLang, 127.0.0.1:30010) only answers requests that carry its API key, which only root holds
(/run/live/engine.key); this gateway is what the box exposes. It serves the part of SGLang's native API that teacher scoring uses:
  POST /generate      {"input_ids": [...]} or {"text": "..."} (or batched lists), "sampling_params" with
                      max_new_tokens=0, "return_logprob", "logprob_start_len"   -> SGLang's reply, unchanged
  GET  /health, /health_generate, /get_model_info, /model_info
Text inputs are tokenized here the way SGLang's tokenizer manager does it (tokenizer(text) for a fast tokenizer,
tokenizer.encode(text) otherwise) and forwarded as ids. With --log, every scored sequence (ids, logprob_start_len,
returned log-probs) is appended to a gzip'd JSON-lines file.

    gateway.py --port P --tokenizer DIR [--upstream URL] [--key-file F] [--model-path SHOWN] [--log FILE] [--log-cap B]
"""
import argparse
import asyncio
import gzip
import json
import os
import sys

sys.path = [p for p in sys.path if p and not p.startswith(("/app", "/tmp", "/home"))]

import aiohttp  # noqa: E402
from aiohttp import web  # noqa: E402

FORWARD_KEYS = ("sampling_params", "return_logprob", "logprob_start_len", "return_text_in_logprobs")


class Log:
    def __init__(self, path, cap):
        self.f = gzip.open(path, "at", compresslevel=3) if path else None
        self.cap = cap
        self.n = 0
        self.full = False
        self.records = 0

    def write(self, rec):
        if self.f is None or self.full:
            return
        line = json.dumps(rec, separators=(",", ":")) + "\n"
        if self.n + len(line) > self.cap:
            self.full = True
            self.f.write(json.dumps({"truncated": True}) + "\n")
            self.f.flush()
            return
        self.f.write(line)
        self.n += len(line)
        self.records += 1

    def flush(self):
        if self.f is not None:
            self.f.flush()

    def close(self):
        if self.f is not None:
            self.f.close()
            self.f = None


def build_app(a, tok):
    log = Log(a.log, a.log_cap)
    with open(a.key_file) as f:
        key = f.read().strip()
    state = {}

    async def session():
        s = state.get("s")
        if s is None or s.closed:
            s = state["s"] = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(limit=0), headers={"Authorization": f"Bearer {key}"},
                timeout=aiohttp.ClientTimeout(total=None, sock_connect=30))
        return s

    def bad(msg, status=400):
        return web.json_response({"error": msg}, status=status)

    async def generate(request):
        try:
            body = await request.json()
        except Exception:  # noqa: BLE001
            return bad("request body is not JSON")
        if not isinstance(body, dict):
            return bad("request body must be a JSON object")
        if body.get("stream"):
            return bad("streaming is not served by this teacher")
        sp = body.get("sampling_params") or {}
        sps = sp if isinstance(sp, list) else [sp]
        for x in sps:
            if not isinstance(x, dict):
                return bad("sampling_params must be an object")
            try:
                if int(x.get("max_new_tokens", 128) or 0) != 0:
                    return bad("this teacher only scores (max_new_tokens must be 0)")
            except (TypeError, ValueError):
                return bad("bad max_new_tokens")
        if body.get("top_logprobs_num") or body.get("token_ids_logprob") or body.get("token_ids_logprob_positions"):
            return bad("top-k / token-id logprobs are not served by this teacher")
        if body.get("input_ids") is not None:
            ids = body["input_ids"]
            batched = bool(ids) and isinstance(ids[0], list)
            seqs = ids if batched else [ids]
        elif body.get("text") is not None:
            text = body["text"]
            batched = isinstance(text, list)
            texts = text if batched else [text]
            if not all(isinstance(t, str) for t in texts):
                return bad("text must be a string or a list of strings")
            if getattr(tok, "is_fast", False):
                seqs = [list(x) for x in tok(texts)["input_ids"]]
            else:
                seqs = [list(tok.encode(t)) for t in texts]
        else:
            return bad("input_ids or text required")
        try:
            seqs = [[int(t) for t in s] for s in seqs]
        except (TypeError, ValueError):
            return bad("input_ids must be lists of ints")
        fwd = {"input_ids": seqs if batched else seqs[0]}
        for k in FORWARD_KEYS:
            if k in body:
                fwd[k] = body[k]
        try:
            s = await session()
            async with s.post(a.upstream + "/generate", json=fwd) as r:
                status = r.status
                raw = await r.read()
        except aiohttp.ClientError as e:
            return bad(f"teacher engine unavailable ({type(e).__name__})", 503)
        if status != 200:
            return web.Response(body=raw, status=status, content_type="application/json")
        try:
            out = json.loads(raw)
        except ValueError:
            return web.Response(body=raw, status=status, content_type="application/json")
        if log.f is not None:
            outs = out if isinstance(out, list) else [out]
            start = body.get("logprob_start_len", -1)
            starts = start if isinstance(start, list) else [start] * len(seqs)
            for seq, st, o in zip(seqs, starts, outs):
                try:
                    ent = (o.get("meta_info") or {}).get("input_token_logprobs") or []
                    if not ent:
                        continue
                    lp = [e[0] for e in ent]
                    rid = [int(e[1]) for e in ent]
                    st = int(st)
                    log.write({"ids": seq, "s": st, "lp": lp, "match": rid == seq[len(seq) - len(rid):]})
                except Exception:  # noqa: BLE001
                    continue
            log.flush()
        return web.Response(body=raw, status=200, content_type="application/json")

    async def health(request):
        try:
            s = await session()
            async with s.get(a.upstream + "/health", timeout=aiohttp.ClientTimeout(total=10)) as r:
                return web.Response(text="", status=200 if r.status == 200 else 503)
        except Exception:  # noqa: BLE001
            return web.Response(text="", status=503)

    async def model_info(_):
        return web.json_response({"model_path": a.model_path, "tokenizer_path": a.model_path, "is_generation": True})

    async def on_cleanup(_):
        s = state.get("s")
        if s is not None:
            await s.close()
        log.close()

    app = web.Application(client_max_size=1 << 30)
    app.router.add_post("/generate", generate)
    app.router.add_get("/health", health)
    app.router.add_get("/health_generate", health)
    app.router.add_get("/get_model_info", model_info)
    app.router.add_get("/model_info", model_info)
    app.on_cleanup.append(on_cleanup)
    return app


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--upstream", default="http://127.0.0.1:30010")
    ap.add_argument("--key-file", default="/run/live/engine.key")
    ap.add_argument("--tokenizer", required=True)
    ap.add_argument("--model-path", default="/models/Falcon-H1R-7B")
    ap.add_argument("--log", default=None)
    ap.add_argument("--log-cap", type=int, default=3 << 30)
    ap.add_argument("--ready-file", default=None)
    a = ap.parse_args()
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    from transformers import AutoTokenizer

    tok = AutoTokenizer.from_pretrained(a.tokenizer)

    async def ready(_app):
        if a.ready_file:
            with open(a.ready_file, "w") as f:
                f.write("ok\n")

    app = build_app(a, tok)
    app.on_startup.append(ready)
    web.run_app(app, host=a.host, port=a.port, print=None, access_log=None, handle_signals=True)


if __name__ == "__main__":
    main()
