#!/bin/bash
LOGFILE="/opt/procfleet/logs/data_processor_$$.log"
echo "data_processor started with PID $$" >> "$LOGFILE"

trap 'echo "data_processor $$ shutting down" >> "$LOGFILE"; exit 0' TERM

while true; do
    echo "$(date): data_processor $$ processing data" >> "$LOGFILE"
    sleep 60 &
    sleep 3
done
