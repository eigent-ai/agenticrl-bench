#!/bin/bash
LOG_FILE="/opt/monitor/logs/health.log"
while true; do
    COLORS=$(tput colors 2>/dev/null || echo "unknown")
    echo "$(date '+%Y-%m-%d %H:%M:%S') status=OK colors=$COLORS" >> "$LOG_FILE"
    sleep 5
done
