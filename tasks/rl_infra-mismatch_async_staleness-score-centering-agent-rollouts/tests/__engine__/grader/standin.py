import os
import sys
sys.path[:] = [p for p in sys.path if not (os.path.realpath(p or ".") + "/").startswith("/app/")]
sys.meta_path[:] = [f for f in sys.meta_path if "__editable__" not in str(getattr(f, "__module__", ""))]
import argparse
import copy
import json
import math
import threading
import numpy as np
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import Rollout, load_index
ap = argparse.ArgumentParser()
ap.add_argument("--data", required=True)
ap.add_argument("--port", type=int, default=30777)
ap.add_argument("--events", required=True)
ap.add_argument("--tokenizer", default="/models/Qwen3.5-2B")
a = ap.parse_args()
from transformers import AutoTokenizer
TOK = AutoTokenizer.from_pretrained(a.tokenizer, trust_remote_code=True)
INDEX = load_index(a.data)
app = FastAPI()
STATE = {"uid": None, "ro": None}
LOCK = threading.Lock()
EV = open(a.events, "a")
K_REC = 128
_tok_cache = {}
def event(kind, **kw):
    with LOCK:
        EV.write(json.dumps({"kind": kind, "uid": STATE["uid"], **kw}) + "\n")
        EV.flush()
def tok_text(t):
    t = int(t)
    if t not in _tok_cache:
        _tok_cache[t] = TOK.decode([t], skip_special_tokens=False)
    return _tok_cache[t]
def error(msg, code=400):
    event("error", msg=msg)
    return JSONResponse({"object": "error", "message": msg, "type": "BadRequestError", "code": code}, status_code=code)
def find_call(input_ids):
    ro = STATE["ro"]
    if ro is None:
        return None, None
    ids = np.asarray(input_ids, dtype=np.int64)
    for k, c in enumerate(ro.meta["calls"]):
        rec = ro.call_input_ids(k)
        if len(rec) == len(ids) and np.array_equal(rec, ids):
            return ro, k
    return ro, None
def check_sampling(rec_req, temperature, top_p, top_k, min_p, extra):
    if rec_req.get("sampling_params") is not None:
        rs = rec_req["sampling_params"]
    else:
        rs = rec_req
    want_t = float(rs.get("temperature", 1.0))
    want_p = float(rs.get("top_p", 1.0) if rs.get("top_p") is not None else 1.0)
    want_k = int(rs.get("top_k", -1) if rs.get("top_k") is not None else -1)
    got_t = 1.0 if temperature is None else float(temperature)
    got_p = 1.0 if top_p is None else float(top_p)
    got_k = -1 if top_k is None else int(top_k)
    if got_k <= 0:
        got_k = -1
    if not (math.isclose(got_t, want_t, rel_tol=0, abs_tol=1e-9) and math.isclose(got_p, want_p, abs_tol=1e-9)
            and got_k == want_k):
        return f"sampling parameters (temperature={got_t}, top_p={got_p}, top_k={got_k}) differ from this generation"
    if min_p not in (None, 0, 0.0):
        return "min_p differs from this generation"
    for name, neutral in (("frequency_penalty", 0.0), ("presence_penalty", 0.0), ("repetition_penalty", 1.0)):
        v = extra.get(name)
        if v is not None and float(v) != neutral:
            return f"{name} differs from this generation"
    for name in ("logit_bias", "custom_logit_processor", "json_schema", "regex", "ebnf", "structural_tag"):
        if extra.get(name):
            return f"{name} is not supported by this replay"
    return None
def meta_arrays(ro, k, n, *, return_logprob, top_n, sampling_mask, mode, with_text):
    sl = ro.call_out(k)
    rows = range(sl.start, sl.start + n)
    m = {}
    ids = ro.a["out_ids"]
    lps = ro.a["out_logp"]
    def entry(lp, t):
        return [float(lp), int(t), tok_text(t) if with_text else None]
    if return_logprob:
        m["output_token_logprobs"] = [entry(lps[r], ids[r]) for r in rows]
    if top_n:
        tids, tlps = ro.a["top_ids"], ro.a["top_logp"]
        m["output_top_logprobs"] = [
            [entry(tlps[r, j], tids[r, j]) for j in range(min(top_n, K_REC)) if tids[r, j] >= 0] for r in rows
        ]
    if sampling_mask:
        o = ro.a["sup_off"]
        if o[sl.start + n] == o[sl.start] and n > 0:
            return None
        sup, slp = [], []
        for r in rows:
            s_ids = ro.a["sup_ids"][o[r]:o[r + 1]]
            s_lp = ro.a["sup_logp"][o[r]:o[r + 1]]
            sup.append([int(x) for x in s_ids])
            if mode == "support":
                slp.append([float(x) for x in s_lp])
            else:
                j = int(np.where(s_ids == ids[r])[0][0])
                slp.append(float(s_lp[j]))
        m["output_token_sampling_mask"] = sup
        m["output_token_sampling_logprobs"] = slp
        m["output_token_sampling_mask_length"] = n
    return m
@app.post("/_replay/select")
async def select(request: Request):
    body = await request.json()
    uid = body["uid"]
    with LOCK:
        STATE["uid"] = uid
        STATE["ro"] = Rollout(a.data, uid, INDEX[uid]) if uid is not None else None
    return {"ok": True}
@app.get("/health")
@app.get("/health_generate")
async def health():
    return JSONResponse({})
@app.get("/get_model_info")
@app.get("/model_info")
async def model_info():
    return {"model_path": "/models/Qwen3.5-2B", "tokenizer_path": "/models/Qwen3.5-2B", "is_generation": True,
            "preferred_sampling_params": None, "weight_version": "default", "has_image_understanding": True,
            "has_audio_understanding": False, "model_type": "qwen3_5", "architectures": ["Qwen3_5ForConditionalGeneration"]}
@app.get("/v1/models")
async def models():
    return {"object": "list", "data": [{"id": "default", "object": "model", "owned_by": "sglang", "root": "default"}]}
@app.api_route("/flush_cache", methods=["GET", "POST"])
async def flush():
    return JSONResponse({})
@app.post("/generate")
async def generate(request: Request):
    body = await request.json()
    if body.get("input_ids") is None:
        return error("this replay serves token-in requests only (input_ids)")
    ro, k = find_call(body["input_ids"])
    if k is None:
        return error("no recorded generation for these input_ids")
    call = ro.meta["calls"][k]
    if call["kind"] != "generate":
        return error("this generation was recorded on /v1/chat/completions")
    sp = body.get("sampling_params") or {}
    msg = check_sampling(call["req"], sp.get("temperature"), sp.get("top_p"), sp.get("top_k"), sp.get("min_p"), sp)
    if msg:
        return error(msg)
    n_rec = call["n_out"]
    max_new = sp.get("max_new_tokens")
    n = n_rec if max_new is None else max(0, min(n_rec, int(max_new)))
    top_n = int(body.get("top_logprobs_num") or 0)
    if top_n > K_REC:
        event("top_n_over_recorded", top_n=top_n)
    mode = body.get("sampling_logprobs_mode") or "selected"
    want_mask = bool(body.get("return_sampling_mask"))
    m = meta_arrays(ro, k, n, return_logprob=bool(body.get("return_logprob")), top_n=top_n,
                    sampling_mask=want_mask, mode=mode, with_text=bool(body.get("return_text_in_logprobs")))
    if m is None:
        return error("sampling support capture is unavailable for this generation (no top-p/top-k filtering)")
    resp = copy.deepcopy(call["resp"])
    meta = resp["meta_info"]
    for key in list(meta):
        if isinstance(meta[key], str) and meta[key].startswith("<npz:"):
            meta[key] = None
    for key in ("output_token_logprobs", "output_top_logprobs", "output_token_sampling_mask",
                "output_token_sampling_logprobs", "output_token_sampling_mask_length"):
        meta.pop(key, None)
    meta.update(m)
    meta["output_token_logprobs_length"] = n if body.get("return_logprob") else 0
    out_ids = [int(x) for x in ro.a["out_ids"][ro.call_out(k).start: ro.call_out(k).start + n]]
    if n < n_rec:
        meta["finish_reason"] = {"type": "length", "length": n}
        meta["completion_tokens"] = n
        spans = []
        for span in meta.get("weight_versions") or []:
            if isinstance(span, dict) and span.get("start", 0) < n:
                spans.append({**span, "end": min(int(span.get("end", n)), n)})
        if meta.get("weight_versions") is not None:
            meta["weight_versions"] = spans
        resp["text"] = TOK.decode(out_ids, skip_special_tokens=bool(sp.get("skip_special_tokens", True)))
    resp["output_ids"] = out_ids
    event("served", endpoint="generate", call=k, n=n, top_n=top_n, mask=want_mask, mode=mode)
    return JSONResponse(resp)
@app.post("/v1/chat/completions")
async def chat(request: Request):
    body = await request.json()
    if body.get("input_ids") is None:
        return error("this replay serves session-server requests only (input_ids)")
    ro, k = find_call(body["input_ids"])
    if k is None:
        return error("no recorded generation for these input_ids")
    call = ro.meta["calls"][k]
    if call["kind"] != "chat":
        return error("this generation was recorded on /generate")
    msg = check_sampling(call["req"], body.get("temperature"), body.get("top_p"), body.get("top_k"),
                         body.get("min_p"), body)
    if msg:
        return error(msg)
    n = call["n_out"]
    mx = body.get("max_tokens") or body.get("max_completion_tokens")
    if mx is not None and int(mx) < n:
        return error("max_tokens below the recorded completion is not supported by this replay")
    top_n = int(body.get("top_logprobs") or 0)
    if top_n > K_REC:
        event("top_n_over_recorded", top_n=top_n)
    mode = body.get("sampling_logprobs_mode") or "selected"
    want_mask = bool(body.get("return_sampling_mask"))
    if want_mask and not body.get("return_meta_info"):
        return error("return_sampling_mask requires return_meta_info=true.")
    resp = copy.deepcopy(call["resp"])
    ch = resp["choices"][0]
    if body.get("return_meta_info"):
        m = meta_arrays(ro, k, n, return_logprob=bool(body.get("logprobs")), top_n=top_n if body.get("logprobs") else 0,
                        sampling_mask=want_mask, mode=mode, with_text=True)
        if m is None:
            return error("sampling support capture is unavailable for this generation (no top-p/top-k filtering)")
        meta = ch["meta_info"]
        for key in list(meta):
            if isinstance(meta[key], str) and meta[key].startswith("<npz:"):
                meta[key] = None
        for key in ("output_token_logprobs", "output_top_logprobs", "output_token_sampling_mask",
                    "output_token_sampling_logprobs", "output_token_sampling_mask_length"):
            meta.pop(key, None)
        meta.update(m)
        meta["output_token_logprobs_length"] = n if body.get("logprobs") else 0
    else:
        ch.pop("meta_info", None)
    if body.get("logprobs"):
        sl = ro.call_out(k)
        content = []
        for r in range(sl.start, sl.start + n):
            t = int(ro.a["out_ids"][r])
            s = tok_text(t)
            item = {"token": s, "bytes": list(s.encode("utf-8")), "logprob": float(ro.a["out_logp"][r]),
                    "top_logprobs": []}
            for j in range(min(top_n, K_REC)):
                tj = int(ro.a["top_ids"][r, j])
                if tj < 0:
                    continue
                sj = tok_text(tj)
                item["top_logprobs"].append({"token": sj, "bytes": list(sj.encode("utf-8")),
                                             "logprob": float(ro.a["top_logp"][r, j])})
            content.append(item)
        ch["logprobs"] = {"content": content}
    else:
        ch["logprobs"] = None
    event("served", endpoint="chat", call=k, n=n, top_n=top_n, mask=want_mask, mode=mode)
    return JSONResponse(resp)
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def other(path: str):
    return error(f"unsupported endpoint /{path} in this replay", code=404)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=a.port, log_level="warning")
