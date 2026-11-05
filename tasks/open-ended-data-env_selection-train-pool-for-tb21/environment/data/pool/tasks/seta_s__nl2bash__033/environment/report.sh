#!/bin/bash
# Report generator — summarises /var/log/monitor/alerts.log

LOG=/var/log/monitor/alerts.log

if [ ! -f "$LOG" ] || [ ! -s "$LOG" ]; then
    echo "Total alerts: 0"
    echo "Processes: (none)"
    echo "Max RSS (MB): 0"
    exit 0
fi

total=$(grep -c "ALERT:" "$LOG")
echo "Total alerts: $total"

echo "Processes: (not implemented)"

max_rss=0
echo "Max RSS (MB): $max_rss"
