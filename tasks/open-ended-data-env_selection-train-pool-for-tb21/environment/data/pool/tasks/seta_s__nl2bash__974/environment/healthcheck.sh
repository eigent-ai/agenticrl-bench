#!/bin/bash
# Health check - determines service status from process state

RUN_DIR="/opt/procmon/run"

for pidfile in "$RUN_DIR"/*.pid; do
    [ -f "$pidfile" ] || continue
    pid=$(cat "$pidfile")
    svc_name=$(basename "$pidfile" .pid)

    if kill -0 "$pid" 2>/dev/null; then
        # Get process state from detailed ps output
        state=$(ps -eo pid,ppid,user,ni,vsz,rss,tty,stat,start,time,comm | awk -v p="$pid" '$1 == p {print $3}')
        echo "$svc_name:running:$state"
    else
        echo "$svc_name:stopped:-"
    fi
done
