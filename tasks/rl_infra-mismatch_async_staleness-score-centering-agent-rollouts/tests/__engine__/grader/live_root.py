import json
import os
import socket
import subprocess
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import numpy as np
FORWARD = ("/generate", "/v1/chat/completions", "/health", "/health_generate", "/get_model_info", "/model_info",
           "/v1/models", "/get_server_info", "/server_info", "/flush_cache", "/abort_request")
GEN = ("/generate", "/v1/chat/completions")
K = 128
TEMPLATE = "miles/utils/chat_template_utils/templates/qwen3.5_fixed.jinja"
def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p
class Proxy:
    def __init__(self, engine_url, api_key):
        self.engine_url = engine_url
        self.auth = {"Authorization": f"Bearer {api_key}"}
        self.lock = threading.Lock()
        self.tag = None
        self.records = []
        self.refused = []
        proxy = self
        class H(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"
            disable_nagle_algorithm = True
            def log_message(self, *a):
                pass
            def _reply(self, code, body, ctype="application/json"):
                self.send_response(code)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            def _do(self, method):
                path = self.path.split("?")[0]
                n = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(n) if n else b""
                if path == "/_live/begin" and method == "POST":
                    try:
                        uid = json.loads(raw or b"{}").get("uid")
                    except ValueError:
                        return self._reply(400, b'{"error": "bad json"}')
                    with proxy.lock:
                        proxy.tag = uid if isinstance(uid, str) else None
                    return self._reply(200, b'{"ok": true}')
                if not path.startswith(FORWARD):
                    with proxy.lock:
                        proxy.refused.append(f"{method} {path}")
                    return self._reply(403, b'{"error": "refused by the verifier"}')
                with proxy.lock:
                    tag = proxy.tag
                req = urllib.request.Request(proxy.engine_url + self.path, data=raw if method != "GET" else None,
                                             method=method,
                                             headers={"Content-Type": self.headers.get("Content-Type") or
                                                      "application/json", **proxy.auth})
                try:
                    with urllib.request.urlopen(req, timeout=1800) as r:
                        code, body, ctype = r.status, r.read(), r.headers.get("Content-Type") or "application/json"
                except urllib.error.HTTPError as e:
                    code, body, ctype = e.code, e.read(), e.headers.get("Content-Type") or "text/plain"
                except Exception as e:
                    return self._reply(502, json.dumps({"error": repr(e)[:300]}).encode())
                if path in GEN:
                    with proxy.lock:
                        proxy.records.append({"tag": tag, "path": path, "code": code, "req": raw, "resp": body})
                return self._reply(code, body, ctype)
            def do_GET(self):
                self._do("GET")
            def do_POST(self):
                self._do("POST")
        self.server = ThreadingHTTPServer(("127.0.0.1", free_port()), H)
        self.server.daemon_threads = True
        self.port = self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
    def stop(self):
        self.server.shutdown()
        self.server.server_close()
def engine_cmd(py, boot, pristine, port, api_key):
    return [py, "-I", boot, "--path", pristine, "--module", "sglang.launch_server", "--api-key", api_key,
            "--model-path", "/models/Qwen3.5-2B", "--trust-remote-code", "--random-seed", "1",
            "--skip-server-warmup", "--enable-metrics", "--host", "127.0.0.1", "--port", str(port),
            "--quantization", "fp8", "--mem-fraction-static", "0.6", "--tool-call-parser", "qwen3_coder",
            "--chat-template", os.path.join(pristine, TEMPLATE)]
def wait_engine(url, proc, api_key, secs=900):
    t = time.time()
    while time.time() - t < secs:
        if proc.poll() is not None:
            return False
        try:
            body = json.dumps({"input_ids": [1, 2, 3], "sampling_params": {"max_new_tokens": 1}}).encode()
            req = urllib.request.Request(url + "/generate", data=body, headers={"Content-Type": "application/json",
                                                                               "Authorization": f"Bearer {api_key}"})
            with urllib.request.urlopen(req, timeout=30) as r:
                if r.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(3)
    return False
def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)
def parse_record(rec):
    if rec["code"] != 200:
        return None
    req = json.loads(rec["req"])
    resp = json.loads(rec["resp"])
    ids = req.get("input_ids")
    if not isinstance(ids, list) or not ids or not all(type(t) is int for t in ids):
        return None
    if rec["path"] == "/generate":
        sp = req.get("sampling_params") or {}
        meta = resp.get("meta_info") or {}
    else:
        sp = req
        meta = (resp.get("choices") or [{}])[0].get("meta_info") or {}
    out = meta.get("output_token_logprobs") or []
    top = meta.get("output_top_logprobs")
    sup = meta.get("output_token_sampling_mask")
    slp = meta.get("output_token_sampling_logprobs")
    toks = []
    for j, e in enumerate(out):
        tok = {"id": int(e[1]), "logp": float(e[0]), "top": None, "sup": None, "sup_logp": None, "sel_logp": None}
        if isinstance(top, list) and j < len(top) and isinstance(top[j], list):
            tok["top"] = [(float(x[0]), int(x[1])) for x in top[j] if isinstance(x, list) and _num(x[0])]
        if isinstance(sup, list) and j < len(sup) and isinstance(sup[j], list):
            tok["sup"] = [int(x) for x in sup[j]]
            if isinstance(slp, list) and j < len(slp) and isinstance(slp[j], list):
                tok["sup_logp"] = [float(x) for x in slp[j]]
            elif isinstance(slp, list) and j < len(slp) and _num(slp[j]):
                tok["sel_logp"] = float(slp[j])
        toks.append(tok)
    params = {"temperature": sp.get("temperature"), "top_p": sp.get("top_p"), "top_k": sp.get("top_k")}
    return ids, params, toks
def support_from_top(t):
    """Support log-probs from the engine's own candidates renormalised over its own sampling mask: what a tree gets
    with top_logprobs + return_sampling_mask instead of sampling_logprobs_mode="support". None unless the candidates
    cover the support and reproduce the engine's support-normalised log-prob of the sampled token."""
    if t["sup"] is None or t["top"] is None or t["sel_logp"] is None or len(set(t["sup"])) != len(t["sup"]):
        return None
    lp = dict((i, l) for l, i in t["top"])
    if len(lp) != len(t["top"]) or t["id"] not in t["sup"] or any(i not in lp for i in t["sup"]):
        return None
    x = np.array([lp[i] for i in t["sup"]], dtype=np.float64)
    x -= x.max() + np.log(np.exp(x - x.max()).sum())
    if abs(x[t["sup"].index(t["id"])] - t["sel_logp"]) > 1e-4:
        return None
    return x.tolist()
def _same_sampling(params, case):
    t = 1.0 if params["temperature"] is None else float(params["temperature"])
    p = 1.0 if params["top_p"] is None else float(params["top_p"])
    k = -1 if params["top_k"] in (None, 0) or int(params["top_k"]) <= 0 else int(params["top_k"])
    return abs(t - case["temperature"]) < 1e-9 and abs(p - case["top_p"]) < 1e-9 and k == case["top_k"]
def build_live(case, samples, records, out_dir):
    uids = [f"{case['id'].replace('-', '_')}_{gi}_{j}" for gi, g in enumerate(case["prompts"]) for j in range(len(g))]
    by_uid = {}
    for s in samples if isinstance(samples, list) else []:
        if isinstance(s, dict) and s.get("uid") in uids:
            if s["uid"] in by_uid:
                raise ValueError(f"{s['uid']}: more than one training sample for one conversation")
            by_uid[s["uid"]] = s
    if set(by_uid) != set(uids):
        raise ValueError(f"live samples missing: {sorted(set(uids) - set(by_uid))[:4]}")
    calls = {}
    for rec in records:
        if rec["tag"] in by_uid:
            try:
                parsed = parse_record(rec)
            except (ValueError, KeyError, TypeError, IndexError):
                parsed = None
            if parsed is not None:
                calls.setdefault(rec["tag"], []).append(parsed)
    support = case["recipe"] == "session"
    index, rewards = {}, {}
    os.makedirs(os.path.join(out_dir, "rollouts"), exist_ok=True)
    for gi, g in enumerate(case["prompts"]):
        for j in range(len(g)):
            uid = f"{case['id'].replace('-', '_')}_{gi}_{j}"
            s = by_uid[uid]
            tokens, resp, mask = s["tokens"], s["response_length"], s["loss_mask"]
            if not (isinstance(tokens, list) and all(type(t) is int for t in tokens) and type(resp) is int
                    and 0 < resp <= len(tokens) and isinstance(mask, list) and len(mask) == resp
                    and all(m in (0, 1) for m in mask)):
                raise ValueError(f"{uid}: malformed live sample")
            P = len(tokens) - resp
            gen = {}
            for ids, params, toks in calls.get(uid, []):
                L = len(ids)
                if L > len(tokens) or tokens[:L] != ids:
                    continue
                n = 0
                while n < len(toks) and L + n < len(tokens) and toks[n]["id"] == tokens[L + n]:
                    n += 1
                if not n:
                    continue
                if not _same_sampling(params, case):
                    raise ValueError(f"{uid}: a generation used sampling parameters other than the recipe's ({params})")
                for q in range(n):
                    gen.setdefault(L + q, toks[q])
            rows, row_of_resp = [], []
            for i in range(resp):
                t = gen.get(P + i)
                if mask[i] == 1 and t is None:
                    raise ValueError(f"{uid}: trained token {i} was not generated by the engine in this conversation")
                row_of_resp.append(len(rows) if mask[i] == 1 else -1)
                if mask[i] == 1:
                    rows.append(t)
            if not rows:
                raise ValueError(f"{uid}: no trained token")
            n = len(rows)
            out_ids = np.array([t["id"] for t in rows], dtype=np.int64)
            out_logp = np.array([t["logp"] for t in rows], dtype=np.float64)
            top_ids = np.full((n, K), -1, dtype=np.int64)
            top_logp = np.full((n, K), -np.inf, dtype=np.float64)
            sup_off, sup_ids, sup_logp, kept_off, kept_ids = [0], [], [], [0], []
            for r, t in enumerate(rows):
                if support:
                    if t["sup_logp"] is None:
                        t["sup_logp"] = support_from_top(t)
                    if t["sup"] is None or t["sup_logp"] is None or len(t["sup"]) != len(t["sup_logp"]) \
                            or t["id"] not in t["sup"] or len(set(t["sup"])) != len(t["sup"]):
                        raise ValueError(f"{uid}: the engine returned neither support-mode log-probs nor candidates "
                                         f"covering the sampling support for a trained token (not requested at "
                                         f"generation time)")
                    sup_ids.extend(t["sup"])
                    sup_logp.extend(t["sup_logp"])
                    kept = set(t["sup"])
                else:
                    if t["top"] is None or len(t["top"]) < K:
                        raise ValueError(f"{uid}: the engine returned fewer than {K} candidate log-probs for a trained "
                                         f"token (not requested at generation time)")
                    top = sorted(t["top"], key=lambda x: -x[0])[:K]
                    top_ids[r] = [x[1] for x in top]
                    top_logp[r] = [x[0] for x in top]
                    if len(set(top_ids[r].tolist())) != K:
                        raise ValueError(f"{uid}: duplicate candidate ids from the engine")
                    kept = set(top_ids[r].tolist())
                sup_off.append(len(sup_ids))
                kept_ids.extend(sorted(kept | {t["id"]}))
                kept_off.append(len(kept_ids))
            np.savez(os.path.join(out_dir, "rollouts", f"{uid}.npz"),
                     out_ids=out_ids, out_logp=out_logp, top_ids=top_ids, top_logp=top_logp,
                     sup_off=np.array(sup_off, dtype=np.int64), sup_ids=np.array(sup_ids, dtype=np.int64),
                     sup_logp=np.array(sup_logp, dtype=np.float64), kept_off=np.array(kept_off, dtype=np.int64),
                     kept_ids=np.array(kept_ids, dtype=np.int64), kept_z=np.zeros(len(kept_ids), dtype=np.float32),
                     filler=np.zeros(n, dtype=np.float32))
            index[uid] = {"uid": uid, "recipe": case["recipe"], "temperature": case["temperature"],
                          "top_p": case["top_p"], "top_k": case["top_k"], "tokens": tokens, "response_length": resp,
                          "loss_mask": mask, "row_of_resp": row_of_resp, "prompt_len": P}
            rewards[uid] = float(case["live_rewards"][j % len(case["live_rewards"])])
    groups = [[f"{case['id'].replace('-', '_')}_{gi}_{j}" for j in range(len(g))] for gi, g in enumerate(case["prompts"])]
    return index, groups, rewards
