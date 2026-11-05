#!/bin/bash
mkdir -p /opt/pipeline/data
echo $$ > /opt/pipeline/data/worker.pid
while true; do
    echo "$(date +%s): heartbeat" >> /opt/pipeline/data/heartbeat.log
    sleep 1
done
