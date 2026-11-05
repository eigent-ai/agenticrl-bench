#!/bin/bash
# Log monitoring script - checks system logs for suspicious activities
# Deployed by: ops-team
# Last modified: 2024-03-10

LOG_FILE="/var/log/syslog.1"

suspicious=$(grep -E 'ERROR|WARN|CRIT' "$LOG_FILE" | tail -n 1)

if [ -n "$suspicious" ]; then
    echo "Suspicious activities found: $suspicious" | mail -s "Security Alert" admin@corp.internal
fi
