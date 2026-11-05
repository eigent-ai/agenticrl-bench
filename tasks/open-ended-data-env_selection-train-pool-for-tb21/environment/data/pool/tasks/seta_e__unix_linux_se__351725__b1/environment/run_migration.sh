#!/bin/bash
LOG_FILE="/opt/dbdeploy/logs/migration.log"
mkdir -p "$(dirname "$LOG_FILE")"

bash /opt/dbdeploy/db_init.sh

psql -w -c "SELECT current_user, current_database();" >> "$LOG_FILE" 2>&1
psql -w -f /opt/dbdeploy/migrations/001_create_tables.sql >> "$LOG_FILE" 2>&1
psql -w -c "SELECT 'MIGRATE_OK';" >> "$LOG_FILE" 2>&1
