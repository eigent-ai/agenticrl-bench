#!/bin/bash
# Backup all files listed in manifest
OUTPUT_DIR="/opt/pipeline/output"
DATA_DIR="/opt/pipeline/data"
BACKUP_DIR="/opt/pipeline/backup"
rm -rf "$BACKUP_DIR"/*
while read line; do
    cp $DATA_DIR/$line $BACKUP_DIR/
done < "$OUTPUT_DIR/manifest.txt"
echo "Backup complete: $(ls "$BACKUP_DIR" | wc -l) items in backup"
