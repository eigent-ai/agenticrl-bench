#!/bin/bash
set -e
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/mysql"
DATA_DIR="/var/docker/mysql-data"
LOGFILE="/opt/backup/backup.log"

echo "[$(date)] Starting backup" >> "$LOGFILE"
tar -czf "${BACKUP_DIR}/backup_${DATE}.tar.gz" -C "$(dirname ${DATA_DIR})" "$(basename ${DATA_DIR})"
echo "[$(date)] Backup completed: backup_${DATE}.tar.gz" >> "$LOGFILE"
