#!/bin/bash
# Process discovery - identifies running services and their interpreters

RUN_DIR="/opt/procmon/run"

for pidfile in "$RUN_DIR"/*.pid; do
    [ -f "$pidfile" ] || continue
    pid=$(cat "$pidfile")
    svc_name=$(basename "$pidfile" .pid)

    # Skip if process is not running
    if ! kill -0 "$pid" 2>/dev/null; then
        continue
    fi

    # Get interpreter from ps full command output
    interpreter=$(ps -p "$pid" -o args | tail -n +1 | sed 's/([^ ]+).*/\1/' | sed 's|.*/||')

    if [ -n "$interpreter" ]; then
        echo "$svc_name:$interpreter:$pid"
    fi
done
