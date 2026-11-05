#!/bin/bash
miniinit-log "scheduler" "Starting task scheduler..." 2>/dev/null || true

echo $$ > /var/run/miniinit/scheduler.pid 2>/dev/null || true

while true; do
    echo "$(date -Iseconds) scheduler tick" >> /var/log/miniinit/scheduler.log 2>/dev/null
    sleep 60
done
