#!/bin/bash
LOGFILE="/opt/procfleet/logs/log_collector_$$.log"
echo "log_collector started with PID $$" >> "$LOGFILE"

trap 'echo "log_collector $$ shutting down" >> "$LOGFILE"; exit 0' TERM

while true; do
    echo "$(date): log_collector $$ collecting logs" >> "$LOGFILE"
    sleep 5
done
