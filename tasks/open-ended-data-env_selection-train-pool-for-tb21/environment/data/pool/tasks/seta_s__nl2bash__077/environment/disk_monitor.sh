#!/bin/bash

previous_usage="$(cat /var/log/disk_usage.log)"
current_usage="$(df -h / | tail -n 1 | awk '{print $5}')"

if [ "$current_usage" -gt "$previous_usage" ]; then
    echo "Disk usage is increasing rapidly: $current_usage" | mail -s "Disk Usage Trend Alert" user@example.com
fi

echo "$current_usage" > /var/log/disk_usage.log
