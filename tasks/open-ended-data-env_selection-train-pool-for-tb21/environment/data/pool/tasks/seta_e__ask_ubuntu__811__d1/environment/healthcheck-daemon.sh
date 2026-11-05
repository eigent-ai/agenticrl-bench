#!/bin/bash
LOG_FILE="/var/log/healthcheck.log"
echo "$(date): healthcheck starting" >> "$LOG_FILE"
while true; do
    echo "$(date): healthcheck monitoring..." >> "$LOG_FILE"
    sleep 10
done
