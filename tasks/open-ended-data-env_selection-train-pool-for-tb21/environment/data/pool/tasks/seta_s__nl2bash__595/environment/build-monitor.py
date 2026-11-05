#!/usr/bin/env python3
"""Build farm monitoring service - watches worker health and metrics."""
import http.server
import json
import sys
import os


class MonitorHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            response = {'status': 'healthy', 'service': 'build-monitor'}
        elif self.path == '/metrics':
            response = {'uptime_seconds': 0, 'workers_monitored': 0}
        else:
            response = {'status': 'ok', 'service': 'build-monitor', 'version': '2.1.0'}
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        pass


def main():
    port = 9090
    server = http.server.HTTPServer(('0.0.0.0', port), MonitorHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
