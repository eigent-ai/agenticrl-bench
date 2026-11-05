#!/bin/bash
BACKUP_DIR="/var/backups/appserver"
TIMESTAMP=$(date +%Y%m%d%H%M%S)
tar -czf "${BACKUP_DIR}/backup-${TIMESTAMP}.tar.gz" -C /opt/appserver data
