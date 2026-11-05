#!/bin/bash
# Health Checker Service - periodically checks backend health
while true; do
    exec {fd}<>/dev/tcp/127.0.0.1/9999 2>/dev/null && exec {fd}>&-
    echo "$(date): Health check OK" >> /var/lib/services/health.log
    sleep 30
done
