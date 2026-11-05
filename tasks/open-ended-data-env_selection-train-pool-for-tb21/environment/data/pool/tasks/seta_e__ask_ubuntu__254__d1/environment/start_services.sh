#!/bin/bash
# Start a Python HTTP server on port 8000 (localhost only)
python3 -m http.server 8000 --bind 127.0.0.1 > /dev/null 2>&1 &
# Start a Python HTTP server on port 8080 (all interfaces)
python3 -m http.server 8080 --bind 0.0.0.0 > /dev/null 2>&1 &
# Start a netcat listener on port 9999 (localhost only)
while true; do nc -l -s 127.0.0.1 9999; done > /dev/null 2>&1 &
sleep 2
exec "$@"
