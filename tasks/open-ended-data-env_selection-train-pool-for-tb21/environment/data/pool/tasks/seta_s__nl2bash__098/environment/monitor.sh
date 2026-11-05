#!/bin/bash

THRESHOLD=100
LOG="/var/log/netmon/traffic.log"
ALERTS="/var/log/netmon/alerts.log"

while IFS= read -r line; do
    rate=$(echo "$line" | awk '{print $5}')
    iface=$(echo "$line" | awk '{print $2}')
    ts=$(echo "$line" | awk '{print $1}')

    if [ "$rate" \> "$THRESHOLD" ]; then
        echo "ALERT $ts $iface $traffic KB/s exceeds threshold $THRESHOLD KB/s" >> "$ALERTS"
    fi
done < "$LOG"
