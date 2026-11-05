#!/bin/bash
BACKUP_DIR="/opt/backups"
MARKER="${BACKUP_DIR}/logs/full_backup_$(date +\%Y\%m\%d).marker"
touch "$MARKER"
echo "Full backup completed at $(date)" >> "${BACKUP_DIR}/logs/full_backup.log"
