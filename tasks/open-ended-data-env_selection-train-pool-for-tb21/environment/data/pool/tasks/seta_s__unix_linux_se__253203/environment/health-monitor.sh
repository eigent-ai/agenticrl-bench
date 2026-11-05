#!/bin/bash
while true; do
    echo "$(date +%Y-%m-%dT%H:%M:%S) status=ok uptime=$(uptime -p)"
    sleep 5
done
