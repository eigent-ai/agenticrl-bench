#!/bin/bash

LOGFILE="/var/log/monitor/diskstats.log"
mkdir -p /var/log/monitor

while true; do
    iostat -x >> "$LOGFILE"
    sleep 0.1
done
