#!/bin/bash
# Log Rotator Service
while true; do
    echo "[$(date)] Log rotation check complete" >> /var/log/svcmgr/log_rotator.log
    sleep 5
done
