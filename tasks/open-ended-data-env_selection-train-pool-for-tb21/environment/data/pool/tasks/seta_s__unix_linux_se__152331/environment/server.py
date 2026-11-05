#!/usr/bin/env python3
import http.server
import socketserver
import json

BIND_HOST = "172.16.100.1"
BIND_PORT = 7777


class LabHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            body = json.dumps(
                {"status": "ok", "service": "lab-metrics"}
            ).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        pass


with socketserver.TCPServer((BIND_HOST, BIND_PORT), LabHandler) as httpd:
    httpd.serve_forever()
