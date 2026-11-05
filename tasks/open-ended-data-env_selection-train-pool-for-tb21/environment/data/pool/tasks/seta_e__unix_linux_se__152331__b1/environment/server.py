#!/usr/bin/env python3
import http.server
import socketserver
import json

BIND_HOST = "10.200.0.2"
BIND_PORT = 9090


class MonitorHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = json.dumps(
                {"status": "healthy", "service": "ns-monitor"}
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


with socketserver.TCPServer((BIND_HOST, BIND_PORT), MonitorHandler) as httpd:
    httpd.serve_forever()
