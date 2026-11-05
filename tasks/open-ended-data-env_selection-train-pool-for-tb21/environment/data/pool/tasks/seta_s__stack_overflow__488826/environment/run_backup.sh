#!/bin/bash

BACKUP_DIR="/tmp/backup"
mkdir -p "$BACKUP_DIR"

while true; do
    find / -type f -name '*.log' 2>/dev/null | while read -r logfile; do
        cp "$logfile" "$BACKUP_DIR/$(basename "$logfile").$(date +%s)"
    done
    sleep 300
done
