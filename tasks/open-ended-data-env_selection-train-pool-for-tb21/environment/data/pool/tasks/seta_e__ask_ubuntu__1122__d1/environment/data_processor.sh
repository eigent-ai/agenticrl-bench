#!/bin/bash
# Data Processor Service
while true; do
    echo "[$(date)] Processing data batch..." >> /var/log/svcmgr/data_processor.log
    sleep 5
done
