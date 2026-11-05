#!/bin/bash
BACKUP_DIR="/opt/backups"
find "${BACKUP_DIR}/logs/" -name "*.tmp" -mtime +7 -delete 2>/dev/null
echo "Weekday cleanup completed at $(date)" >> "${BACKUP_DIR}/logs/cleanup.log"
