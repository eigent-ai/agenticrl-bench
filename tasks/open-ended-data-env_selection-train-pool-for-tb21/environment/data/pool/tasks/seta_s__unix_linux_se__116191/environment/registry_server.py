#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

os.chdir('/opt/services/registry_data')
httpd = HTTPServer(('0.0.0.0', 9091), SimpleHTTPRequestHandler)
httpd.serve_forever()
