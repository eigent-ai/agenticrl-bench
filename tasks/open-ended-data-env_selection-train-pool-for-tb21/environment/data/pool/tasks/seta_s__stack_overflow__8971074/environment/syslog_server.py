#!/usr/bin/env python3
"""Simple UDP syslog receiver for testing."""

import logging
import socketserver

LOG_FILE = '/opt/monitor/syslog_received.log'
HOST, PORT = '127.0.0.1', 5140

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    filename=LOG_FILE,
    filemode='a'
)

class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip().decode('utf-8', errors='replace')
        logging.info(data)

if __name__ == '__main__':
    server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
    print(f'Syslog receiver listening on {HOST}:{PORT}')
    server.serve_forever()
