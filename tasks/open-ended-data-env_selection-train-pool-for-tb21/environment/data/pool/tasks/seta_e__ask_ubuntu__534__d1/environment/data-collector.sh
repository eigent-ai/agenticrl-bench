#!/bin/bash
while true; do
    echo "$(date): Collecting data - load=$(cat /proc/loadavg | awk '{print $1}')" >> /var/log/data-collector.log
    sleep 5
done
