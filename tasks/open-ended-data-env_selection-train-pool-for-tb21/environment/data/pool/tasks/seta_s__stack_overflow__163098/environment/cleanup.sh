#!/bin/bash
# Cleans up old transaction logs
# Removes WAL files older than 60 minutes to free disk space

PG_WAL_DIR="/var/lib/postgresql/16/main/pg_wal"

echo "Starting WAL cleanup..."
find "$PG_WAL_DIR" -name "0*" -mmin +60 -delete
echo "Cleanup complete."
exit 0
