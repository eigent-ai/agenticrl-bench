#!/bin/bash
set -e
DB_DIR="/app/db"
DB_PATH="$DB_DIR/reports.db"

rm -f "$DB_PATH"
sqlite3 "$DB_PATH" < "$DB_DIR/schema.sql"
sqlite3 "$DB_PATH" < "$DB_DIR/seed.sql"
echo "Database built at $DB_PATH"
