#!/bin/bash
# Health Checker Service
while true; do
    echo "[$(date)] Health check: OK" >> /var/log/svcmgr/health_checker.log
    sleep 5
done
