#!/bin/bash
LOG_FILE="/var/log/reportgen.log"
echo "$(date): reportgen starting" >> "$LOG_FILE"
while true; do
    echo "$(date): reportgen generating reports..." >> "$LOG_FILE"
    sleep 15
done
