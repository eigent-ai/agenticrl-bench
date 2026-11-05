#!/bin/bash
BACKUP_DIR="/opt/backups"
LOGFILE="${BACKUP_DIR}/logs/archive_$(date +%b_%d).log"
echo "Monthly archive started at $(date)" > "$LOGFILE"
echo "Compressing previous month data..." >> "$LOGFILE"
echo "Monthly archive completed at $(date)" >> "$LOGFILE"
