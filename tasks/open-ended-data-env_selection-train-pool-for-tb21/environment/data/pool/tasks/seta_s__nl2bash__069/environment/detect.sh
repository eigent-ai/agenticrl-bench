#!/bin/bash

THRESHOLD=3
LOG=/var/log/auth.log

grep "Failed password" "$LOG" | while read line; do
    ip_address=$(echo "$line" | awk '{print $11}')
    count=$(grep -c "$ip_address" "$LOG")
    if [ "$count" -gt "$THRESHOLD" ]; then
        iptables -A INPUT -s "$ip_address" -j DROP
    fi
done
