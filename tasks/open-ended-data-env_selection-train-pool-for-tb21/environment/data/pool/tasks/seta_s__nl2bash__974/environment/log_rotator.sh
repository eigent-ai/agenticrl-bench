#!/bin/sh
# Log rotation service

LOGDIR="/opt/procmon/logs"
LOGFILE="/opt/procmon/logs/log_rotator.log"

while true; do
    for f in "$LOGDIR"/*.log; do
        if [[ -f "$f" ]] && [[ $(stat -c%s "$f" 2>/dev/null) -gt 1048576 ]]; then
            echo "$(date '+%Y-%m-%d %H:%M:%S') [log_rotator] rotating: $f" >> "$LOGFILE"
            > "$f"
        fi
    done
    echo "$(date '+%Y-%m-%d %H:%M:%S') [log_rotator] check complete" >> "$LOGFILE"
    sleep 10
done
