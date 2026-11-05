#!/bin/sh
# Log rotation script - clears log files to free up disk space

CONFIG="/etc/log-rotate/rotate.conf"
HISTORY="/var/log/rotation_history.log"

while IFS= read -r logfile; do
    [[ "$logfile" =~ ^#.* ]] && continue
    [[ -z "$logfile" ]] && continue

    if [[ -f "$logfile" ]]; then
        rm -f "$logfile"
        touch "$logfile"
        echo "$(date '+%Y-%m-%d %H:%M:%S') Rotated $logfile" >> "$HISTORY"
    fi
done < "$CONFIG"

echo "Rotation complete."
