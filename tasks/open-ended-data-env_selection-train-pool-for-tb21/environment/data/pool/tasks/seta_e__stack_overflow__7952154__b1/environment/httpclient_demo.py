#!/usr/bin/env python3
"""HTTP client demo with debug logging via fileConfig."""
import logging
import logging.config
import http.client
import requests
import sys

# Load logging configuration from INI file
logging.config.fileConfig('/opt/app/conf/logging.conf')

# Monkey-patch http.client to redirect its print-based debug output to logging
_httpclient_logger = logging.getLogger("http.client")

def _httpclient_log(*args):
    _httpclient_logger.log(logging.DEBUG, " ".join(args))

http.client.print = _httpclient_log
http.client.HTTPConnection.debuglevel = 1

# Make a request
url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080/hello.txt"
response = requests.get(url)
print(f"Response: {response.text.strip()}")
sys.exit(0)
