#!/bin/bash
# Backup Deduplication Script
# Replaces identical files across daily snapshots with hard links

BACKUP_DIR="/srv/backups"
BASE="daily.0"

echo "Starting backup deduplication..."

for file in $(find "$BACKUP_DIR/$BASE" -type f); do
    filename="${file#$BACKUP_DIR/$BASE/}"

    for snap in daily.1 daily.2; do
        target="$BACKUP_DIR/$snap/$filename"
        if [ -f "$target" ]; then
            base_size=$(stat -c '%s' $file)
            target_size=$(stat -c '%s' $target)
            if [ "$base_size" = "$target_size" ]; then
                ln -f $file $target
                echo "Linked: $target -> $file"
            fi
        fi
    done
done

echo "Deduplication complete."
