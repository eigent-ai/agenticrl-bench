#!/bin/bash
# Apache log cleanup script
LOG_DIR="/var/log/apache2"
find "$LOG_DIR" -name "*.log" -mtime +30 -exec rm -f {} \;
echo "$(date): Apache log cleanup completed" >> /var/log/apache-log-cleanup.log
