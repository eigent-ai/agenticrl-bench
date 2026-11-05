#!/usr/bin/env python3
"""In-memory key/value cache daemon (dev)."""
import argparse
import json
import os
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ap = argparse.ArgumentParser()
ap.add_argument("--port", type=int, default=6380)
ap.add_argument("--id-file", help="write this instance's id here")
args = ap.parse_args()
DATA = {}
if args.id_file:
    os.makedirs(os.path.dirname(args.id_file), exist_ok=True)
    with open(args.id_file, "w") as f:
        f.write(str(uuid.uuid4()) + "\n")


class H(BaseHTTPRequestHandler):
    def _send(self, code, body):
        b = body.encode()
        self.send_response(code)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path == "/dump":
            return self._send(200, json.dumps(DATA, sort_keys=True))
        k = self.path[3:] if self.path.startswith("/k/") else None
        if k in DATA:
            return self._send(200, DATA[k])
        self._send(404, "")

    def do_PUT(self):
        n = int(self.headers.get("Content-Length") or 0)
        if self.path.startswith("/k/"):
            DATA[self.path[3:]] = self.rfile.read(n).decode()
            return self._send(200, "OK")
        self._send(404, "")

    def do_DELETE(self):
        DATA.pop(self.path[3:], None)
        self._send(200, "OK")

    def log_message(self, *a):
        pass


print("kvd ready on", args.port, flush=True)
ThreadingHTTPServer(("127.0.0.1", args.port), H).serve_forever()
