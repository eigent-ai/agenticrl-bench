#!/bin/bash
# Log Streamer Service - reads logs periodically
while true; do
    for logfile in /var/log/*.log 2>/dev/null; do
        if [ -f "$logfile" ]; then
            tail -n 5 "$logfile" >> /var/lib/services/streamed.log 2>/dev/null
        fi
    done
    sleep 10
done
