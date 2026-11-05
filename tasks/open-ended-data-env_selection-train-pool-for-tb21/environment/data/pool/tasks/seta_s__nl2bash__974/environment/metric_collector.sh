#!/bin/bash
# Metric collection daemon

LOGFILE="/opt/procmon/logs/metric_collector.log"

while true; do
    load=$(cat /proc/loadavg | awk '{print $1}')
    mem=$(free -m | awk 'NR==2{print $3}')
    echo "$(date '+%Y-%m-%d %H:%M:%S') [metric_collector] load=$load mem_used=${mem}M" >> "$LOGFILE"
    sleep 5
done
