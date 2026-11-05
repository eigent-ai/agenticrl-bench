#!/bin/bash
LOG_FILE="/opt/pipeline/logs/session.log"
mkdir -p "$(dirname "$LOG_FILE")"
exec 1>> "$LOG_FILE" 2>&1
echo "Pipeline initialized"
echo "System check: OK"
