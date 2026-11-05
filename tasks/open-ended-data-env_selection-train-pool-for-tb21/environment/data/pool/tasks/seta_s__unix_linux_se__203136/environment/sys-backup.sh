#!/bin/bash
# sys-backup.sh - System backup script for maintenance toolkit

CONFIG_FILE="/etc/maintenance/backup.conf"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file $CONFIG_FILE not found"
    exit 1
fi

source "$CONFIG_FILE"

if [ -z "$BACKUP_TARGETS" ]; then
    echo "Error: BACKUP_TARGETS not defined in $CONFIG_FILE"
    exit 1
fi

if [ -z "$BACKUP_DEST" ]; then
    echo "Error: BACKUP_DEST not defined in $CONFIG_FILE"
    exit 1
fi

mkdir -p "$BACKUP_DEST"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DEST}/backup_${TIMESTAMP}.tar.gz"

echo "Starting backup at $(date)"
echo "Targets: $BACKUP_TARGETS"
echo "Destination: $BACKUP_FILE"

tar czf "$BACKUP_FILE" $BACKUP_TARGETS 2>/dev/null

if [ $? -eq 0 ]; then
    echo "Backup completed successfully: $BACKUP_FILE"
else
    echo "Warning: Backup completed with some errors"
fi
