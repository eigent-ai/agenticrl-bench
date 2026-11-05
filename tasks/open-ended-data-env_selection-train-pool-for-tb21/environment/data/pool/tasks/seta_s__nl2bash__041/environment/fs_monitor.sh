#!/bin/bash

# Filesystem usage monitor
threshold="80"

file_systems="$(df -h | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{print $4,$5}' | sed 's/%//')"

while read -r line; do
    usage=$(echo "$line" | awk '{print $1}')
    mount_point=$(echo "$line" | awk '{print $2}')
    if [ "$usage" -gt "$threshold" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ALERT: $mount_point is at ${usage}% (threshold: ${threshold}%)" >> /var/log/fs_alerts.log
    fi

done <<< "$file_systems"
