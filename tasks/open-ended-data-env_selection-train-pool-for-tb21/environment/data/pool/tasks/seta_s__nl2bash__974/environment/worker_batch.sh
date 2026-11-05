#!/bin/sh
# Worker batch processing service

declare -a tasks=("process" "transform" "aggregate")
LOGFILE="/opt/procmon/logs/worker_batch.log"

while true; do
    for task in "${tasks[@]}"; do
        echo "$(date '+%Y-%m-%d %H:%M:%S') [worker_batch] executing: $task" >> "$LOGFILE"
    done
    sleep 5
done
