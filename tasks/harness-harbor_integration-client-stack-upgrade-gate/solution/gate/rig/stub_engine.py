import hashlib
import json
import os
import secrets
import socket
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
SCRIPTS = {}
STATE = {}
LOCK = threading.Lock()
OUT = None
ENGINE = {}
RUN_ID = os.environ.get("GATE_RUN_ID", "gate") + "." + secrets.token_hex(4)
def forward(ep, idx, body):
    url = ENGINE.get(ep)
    if not url or not isinstance(body, dict):
        return None
    b = dict(body)
    b.pop("max_completion_tokens", None)
    b.pop("stream_options", None)
    b.update(max_tokens=1, stream=False, rid=f"{RUN_ID}.{ep}.{idx}")
    req = urllib.request.Request(url.rstrip("/") + "/chat/completions", data=json.dumps(b).encode(),
                                 headers={"Content-Type": "application/json"})
    status, resp = None, None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                status, resp = r.status, json.loads(r.read())
            break
        except urllib.error.HTTPError as e:
            status = e.code
            break
        except Exception as e:
            status = f"{type(e).__name__}"
            time.sleep(2 * (attempt + 1))
    ids = ((resp or {}).get("sglext") or {}).get("input_ids")
    sha = hashlib.sha256(",".join(map(str, ids)).encode()).hexdigest() if isinstance(ids, list) else None
    return {"rid": b["rid"], "status": status, "ids": sha}
def classify(body):
    msgs = body.get("messages") or []
    last = ""
    for m in reversed(msgs):
        if m.get("role") == "user":
            c = m.get("content")
            if isinstance(c, list):
                c = "".join(p.get("text", "") for p in c if isinstance(p, dict))
            last = c or ""
            break
    low = last.lower()
    if low.startswith("you are about to hand off your work to another ai agent"):
        return "summary"
    if low.startswith("you are picking up work from a previous ai agent"):
        return "questions"
    if low.startswith("the next agent has a few questions for you"):
        return "answers"
    if low.startswith("briefly continue this task"):
        return "short_summary"
    return "main"
def completion(content, reasoning, finish="stop", n_prompt=0):
    msg = {"role": "assistant", "content": content}
    if reasoning is not None:
        msg["reasoning_content"] = reasoning
    return {
        "id": "chatcmpl-stub",
        "object": "chat.completion",
        "created": 1760000000,
        "model": "policy",
        "choices": [{"index": 0, "message": msg, "finish_reason": finish, "logprobs": None}],
        "usage": {"prompt_tokens": n_prompt, "completion_tokens": max(1, len(content) // 4),
                  "total_tokens": n_prompt + max(1, len(content) // 4)},
    }
CANNED = {
    "summary": "Summary: the previous agent inspected the repository, ran the listed commands and was midway through the task.",
    "questions": "1. Which files were modified?\n2. Which commands failed?\n3. What remains to be done?",
    "answers": "1. None yet.\n2. None.\n3. Finish the task as described.",
    "short_summary": "Continue from the current terminal state and finish the task.",
}
class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def log_message(self, *a):
        pass
    def _send(self, code, obj=None, raw=None, ctype="application/json"):
        b = raw if raw is not None else json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)
    def do_GET(self):
        self._send(200, {"object": "list", "data": [{"id": "policy", "object": "model"}]})
    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n)
        parts = self.path.split("/")
        ep = parts[2] if len(parts) > 2 and parts[1] == "e" else "_"
        try:
            body = json.loads(raw)
        except Exception:
            body = {"_unparsable": raw.decode(errors="replace")}
        script = SCRIPTS.get(ep)
        if script is None:
            p = os.path.join(SCRIPT_DIR, ep + ".json")
            script = json.load(open(p)) if os.path.exists(p) else {"responses": [], "faults": {}}
            SCRIPTS[ep] = script
        with LOCK:
            st = STATE.setdefault(ep, {"n": 0, "main": 0})
            idx = st["n"]
            st["n"] += 1
            kind = classify(body) if isinstance(body, dict) else "main"
            fault = script.get("faults", {}).get(str(idx))
            pers = script.get("persist")
            if fault is None and pers and idx >= int(pers["from"]):
                fault = pers["kind"]
            if fault is None and kind == "main":
                k = st["main"]
                st["main"] += 1
            else:
                k = None
        rec = {"i": idx, "path": "/" + "/".join(parts[3:]), "kind": kind, "fault": fault, "body": body,
               "headers": {k_.lower(): v for k_, v in self.headers.items() if k_.lower() not in ("host", "content-length")}}
        if ENGINE:
            rec["engine"] = forward(ep, idx, body)
        with LOCK:
            with open(os.path.join(OUT, ep + ".jsonl"), "a") as f:
                f.write(json.dumps(rec) + "\n")
        if fault:
            return self._fault(fault)
        if kind != "main":
            return self._send(200, completion(CANNED.get(kind, "ok"), None))
        resp = script.get("responses", [])
        if k is not None and k < len(resp):
            r = resp[k]
        else:
            r = script.get("tail") or {"content": '{"analysis": "Done.", "plan": "Finish.", "commands": [], "task_complete": true}', "reasoning_content": None}
        self._send(200, completion(r["content"], r.get("reasoning_content"), r.get("finish_reason", "stop")))
    def _fault(self, f):
        kind = f["kind"] if isinstance(f, dict) else f
        if kind == "hang":
            time.sleep(float(f.get("secs", 60)) if isinstance(f, dict) else 60.0)
            return self._send(504, {"object": "error", "message": "upstream timed out", "type": "Timeout", "param": None, "code": 504})
        if kind == "http500":
            return self._send(500, {"object": "error", "message": "Internal server error", "type": "InternalServerError", "param": None, "code": 500})
        if kind == "http502":
            return self._send(502, raw=b"<html><body><h1>502 Bad Gateway</h1></body></html>", ctype="text/html")
        if kind == "http503":
            return self._send(503, {"object": "error", "message": "Service Unavailable", "type": "ServiceUnavailableError", "param": None, "code": 503})
        if kind == "http429":
            return self._send(429, {"object": "error", "message": "Too many requests", "type": "RateLimitError", "param": None, "code": 429})
        if kind == "ctx400":
            msg = f.get("message") if isinstance(f, dict) else None
            msg = msg or ("Requested token count exceeds the model's maximum context length of 65536 tokens. "
                          "You requested a total of 66231 tokens: 58039 tokens from the input messages and 8192 "
                          "tokens for the completion. Please reduce the number of tokens in the input messages or "
                          "the completion to fit within the limit.")
            return self._send(400, {"object": "error", "message": msg, "type": "BadRequestError", "param": None, "code": 400})
        if kind == "reset":
            try:
                self.connection.shutdown(socket.SHUT_RDWR)
            except Exception:
                pass
            self.close_connection = True
            return
        if kind == "badjson":
            return self._send(200, raw=b'{"id": "x", "choices": [')
        if kind == "empty_choices":
            return self._send(200, {"id": "x", "object": "chat.completion", "created": 0, "model": "policy", "choices": [],
                                    "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}})
        return self._send(500, {"error": "unknown fault"})
if __name__ == "__main__":
    port, SCRIPT_DIR, OUT = int(sys.argv[1]), sys.argv[2], sys.argv[3]
    os.makedirs(OUT, exist_ok=True)
    if os.environ.get("GATE_ENGINE_MAP"):
        ENGINE.update(json.load(open(os.environ["GATE_ENGINE_MAP"])))
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    srv.daemon_threads = True
    print(f"ready {srv.server_address[1]}", flush=True)
    srv.serve_forever()
