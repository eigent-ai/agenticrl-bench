#!/bin/bash
LOG_FILE="/var/log/dataprocessor.log"
echo "$(date): dataprocessor starting" >> "$LOG_FILE"
while true; do
    echo "$(date): dataprocessor processing data..." >> "$LOG_FILE"
    sleep 5
done
