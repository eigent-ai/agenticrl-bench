#!/bin/bash
# Backup script for forensic compliance
# This script copies files from source to backup directory

SOURCE_DIR="/data/source"
BACKUP_DIR="/data/backup"

# Clear previous backup
rm -rf "$BACKUP_DIR"/*

# Copy files recursively
cp -r "$SOURCE_DIR"/* "$BACKUP_DIR"/

echo "Backup completed."
