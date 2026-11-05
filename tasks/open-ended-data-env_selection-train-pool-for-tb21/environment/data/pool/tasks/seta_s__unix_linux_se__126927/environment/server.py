#!/usr/bin/env python3
"""Simple HTTP server for the web application."""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        config = {}
        conf_path = "/opt/app/config/app.conf"
        if os.path.exists(conf_path):
            with open(conf_path) as f:
                for line in f:
                    line = line.strip()
                    if "=" in line and not line.startswith("#"):
                        key, val = line.split("=", 1)
                        config[key.strip()] = val.strip()

        response = {
            "status": "running",
            "version": config.get("APP_VERSION", "unknown"),
            "server_port": config.get("SERVER_PORT", "8080"),
        }
        body = json.dumps(response).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass  # suppress request logging


def main():
    port = 8080
    server = HTTPServer(("0.0.0.0", port), AppHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
