#!/bin/bash
# WAL archive script for PostgreSQL
# Copies completed WAL segments to the archive directory

WAL_SOURCE="$1"
WAL_FILENAME="$2"
ARCHIVE_DIR="/var/lib/postgresql/wal_archive"

cp "$WAL_SOURCE" "$ARCHIVE_DIR/$WAL_FILENAME"

# Clean up old archived files
/usr/bin/pg_archivecleanup "$ARCHIVE_DIR" "$WAL_FILENAME"
