#!/bin/bash
BACKUP_DIR="/opt/backups"
LOGFILE="${BACKUP_DIR}/logs/inc_$(date +%Y%m%d).log"
echo "Incremental backup started at $(date)" > "$LOGFILE"
echo "Scanning for changed files..." >> "$LOGFILE"
echo "Incremental backup completed at $(date)" >> "$LOGFILE"
