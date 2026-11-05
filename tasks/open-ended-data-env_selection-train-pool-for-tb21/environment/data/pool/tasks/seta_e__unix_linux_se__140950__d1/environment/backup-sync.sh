#!/bin/bash
# Backup sync job
OUTPUT_DIR="/var/spool/jobs/output"
mkdir -p "$OUTPUT_DIR"
echo "Backup sync started: $(date)" > "$OUTPUT_DIR/backup-sync.log"
echo "Syncing files..." >> "$OUTPUT_DIR/backup-sync.log"
sleep 3
echo "Backup sync complete: $(date)" >> "$OUTPUT_DIR/backup-sync.log"
