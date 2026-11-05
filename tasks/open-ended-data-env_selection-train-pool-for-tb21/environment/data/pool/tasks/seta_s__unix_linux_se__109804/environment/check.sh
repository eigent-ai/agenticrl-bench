#!/bin/bash
LOG_DIR="/opt/startmon/logs"
echo "$(date '+%Y-%m-%d %H:%M:%S') Starting health check" >> "${LOG_DIR}/check.log"
python3 /opt/startmon/run_checks.py >> "${LOG_DIR}/check.log" 2>&1
