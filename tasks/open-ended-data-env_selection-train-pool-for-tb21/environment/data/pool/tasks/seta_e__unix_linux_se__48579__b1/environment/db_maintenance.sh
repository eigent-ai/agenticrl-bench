#!/bin/bash
set -e

# Delete expired sessions
psql -U maintuser -d appdb -v ON_ERROR_STOP=1 -c \
  "DELETE FROM app_data.sessions WHERE expires_at < NOW();"

# Purge old audit logs (older than 30 days)
psql -U maintuser -d appdb -v ON_ERROR_STOP=1 -c \
  "DELETE FROM app_data.audit_logs WHERE created_at < NOW() - INTERVAL '30 days';"

# Update maintenance status
psql -U maintuser -d appdb -v ON_ERROR_STOP=1 -c \
  "UPDATE app_data.maintenance_status SET last_run = NOW(), status = 'success' WHERE task_name = 'daily_cleanup';"

echo "Maintenance complete"
