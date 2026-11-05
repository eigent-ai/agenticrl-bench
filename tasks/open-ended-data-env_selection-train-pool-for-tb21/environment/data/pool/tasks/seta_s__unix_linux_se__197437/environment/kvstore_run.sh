#!/bin/bash
miniinit-log "kvstore" "Starting key-value store..." 2>/dev/null || true
exec python3 /opt/miniinit/svcs/kvstore/server.py
