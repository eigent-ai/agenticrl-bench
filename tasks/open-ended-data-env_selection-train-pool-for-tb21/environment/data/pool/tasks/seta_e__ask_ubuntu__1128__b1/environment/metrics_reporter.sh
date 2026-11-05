#!/bin/bash
# Metrics Reporter Service - collects system metrics
while true; do
    echo "$(date): cpu=$(cat /proc/loadavg | cut -d' ' -f1) mem=$(free -m | awk 'NR==2{print $3}')" >> /var/lib/services/metrics.log
    sleep 15
done
