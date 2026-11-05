#!/bin/bash
set -e

SOURCE=/srv/app-data
DEST=/srv/app-backup
LOG=/var/log/backup/sync.log

echo "$(date): Starting sync" >> "$LOG"
rsync -a "$SOURCE/" "$DEST/"
echo "$(date): Sync complete" >> "$LOG"
