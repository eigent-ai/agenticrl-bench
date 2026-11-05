#!/bin/bash
# Metrics Collector Service
while true; do
    echo "[$(date)] Metrics collected" >> /var/log/svcmgr/metrics_collector.log
    sleep 5
done
