#!/bin/bash
set -e

echo "Starting backup..."

echo "Syncing data files..."
doas /opt/backup/bin/sync_data

echo "Restarting backup-svc service..."
doas /usr/sbin/service backup-svc restart

echo "Recording backup timestamp..."
date "+%Y-%m-%d %H:%M:%S" > /opt/backup/.last_backup

echo "Backup completed successfully."
