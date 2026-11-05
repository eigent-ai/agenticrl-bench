#!/usr/bin/env python3
"""Minimal HTTP server for testing httpie."""
import http.server
import threading
import sys

class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status": "ok", "message": "Hello from test server"}')
    def log_message(self, format, *args):
        pass  # suppress logs

def start_server(port=18923):
    server = http.server.HTTPServer(("127.0.0.1", port), TestHandler)
    server.serve_forever()

if __name__ == "__main__":
    start_server()
