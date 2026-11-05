#!/bin/bash
# Health monitoring daemon

LOGFILE="/opt/procmon/logs/health_daemon.log"

while true; do
    uptime_sec=$(cat /proc/uptime | awk '{print $1}')
    echo "$(date '+%Y-%m-%d %H:%M:%S') [health_daemon] uptime=${uptime_sec}s status=ok" >> "$LOGFILE"
    sleep 5
done
