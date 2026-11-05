#!/bin/bash
# Simulated backup script
echo "Running backup at $(date)"
if [[ "$1" == "--fail" ]]; then
    echo "ERROR: Backup failed!"
    exit 1
fi
echo "Backup completed successfully"
exit 0
