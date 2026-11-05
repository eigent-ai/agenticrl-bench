#!/bin/bash
# service-restart.sh - Service restart script for maintenance toolkit

if [ -z "$1" ]; then
    echo "Error: No service name provided"
    echo "Usage: $0 <service-name>"
    exit 1
fi

SERVICE_NAME="$1"

echo "Restarting service: $SERVICE_NAME"

if command -v systemctl &>/dev/null; then
    systemctl restart "$SERVICE_NAME" 2>&1
    STATUS=$?
else
    echo "Warning: systemctl not available, attempting service command"
    service "$SERVICE_NAME" restart 2>&1
    STATUS=$?
fi

if [ $STATUS -eq 0 ]; then
    echo "Service $SERVICE_NAME restarted successfully"
else
    echo "Error: Failed to restart service $SERVICE_NAME (exit code: $STATUS)"
fi

exit $STATUS
