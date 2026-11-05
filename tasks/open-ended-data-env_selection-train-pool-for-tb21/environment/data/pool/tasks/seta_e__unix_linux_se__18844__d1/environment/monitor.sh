#!/bin/bash
WATCH_DIR="/opt/dataproc/logs/"
LOG_FILE="/opt/dataproc/logs/monitor.log"
inotifywait -e access "$WATCH_DIR" | while read dir event file; do
    echo "[$(date)] $event $dir$file" >> "$LOG_FILE"
done
