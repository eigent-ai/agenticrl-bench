#!/bin/bash
# Container entrypoint: start the legacy proxy, then exec the actual command
if ! pgrep -f "legacy-proxy.py" > /dev/null; then
    python3 /opt/legacy-proxy/legacy-proxy.py &
    sleep 1
fi
exec "$@"
