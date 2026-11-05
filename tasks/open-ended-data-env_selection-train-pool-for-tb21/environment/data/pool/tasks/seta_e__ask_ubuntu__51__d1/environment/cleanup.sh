#!/bin/bash
# Cleanup script that generates both stdout and stderr messages

echo "Starting cleanup process..."
echo "Removing temporary files..."

# Simulate cleanup operations
echo "Cleaning /tmp/backup_staging..."
echo "Warning: Could not remove /tmp/backup_staging/locked_file: Resource busy" >&2
echo "Removed 3 temporary files"

echo "Cleaning old log rotations..."
echo "Error: Failed to rotate /var/log/backup_old.log: Permission denied" >&2

echo "Cleanup completed: freed 150KB"
