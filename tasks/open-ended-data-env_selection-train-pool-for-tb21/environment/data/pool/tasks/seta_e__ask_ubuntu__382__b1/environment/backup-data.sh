#!/bin/bash
# Backup script - requires root privileges
echo "$(date '+%Y-%m-%d %H:%M:%S') - Backup executed" >> /var/log/maintenance/backup.log
touch /var/backups/maintenance/backup-$(date +%s)
