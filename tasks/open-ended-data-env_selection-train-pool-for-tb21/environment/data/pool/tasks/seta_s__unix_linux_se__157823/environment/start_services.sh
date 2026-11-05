#!/bin/bash
mkdir -p /run/services
python3 -m http.server 8080 --bind 0.0.0.0 >/dev/null 2>&1 &
echo $! > /run/services/webapp.pid
python3 -m http.server 9090 --bind 0.0.0.0 >/dev/null 2>&1 &
echo $! > /run/services/apiserver.pid
python3 -m http.server 9091 --bind 0.0.0.0 >/dev/null 2>&1 &
echo $! > /run/services/metrics.pid
exec tail -f /dev/null
