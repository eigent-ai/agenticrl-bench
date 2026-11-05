#!/bin/bash
miniinit-log "logger" "Starting log watcher..." 2>/dev/null || true

echo $$ > /var/run/miniinit/logger.pid 2>/dev/null || true

touch /var/log/miniinit/system.log
exec tail -f /var/log/miniinit/system.log
