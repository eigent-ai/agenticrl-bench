#!/bin/bash
# Simulated daemon stop script
PID_FILE="/var/run/dataproc.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID"
    fi
    rm -f "$PID_FILE"
fi

exit 0
