#!/bin/bash
miniinit-log "webapp" "Loading configuration..." 2>/dev/null || true

source /etc/miniinit/webapp.conf 2>/dev/null

if [ -z "$PORT" ]; then
    echo "[webapp] FATAL: PORT not configured - cannot load config" >&2
    exit 1
fi

export PORT KVSTORE_HOST KVSTORE_PORT
exec python3 /opt/miniinit/svcs/webapp/server.py
