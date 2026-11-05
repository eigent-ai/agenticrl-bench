#!/bin/bash

source /etc/log-cleanup.conf

> "$REPORT_FILE"

find "$LOG_DIR" -mtime $RETENTION_DAYS ! -name "*.pid" -o ! -name "*.lock" | while read -r filepath; do
    rm "$filepath" 2>/dev/null
    echo "$filepath" >> "$REPORT_FILE"
done

echo "Cleanup complete."
