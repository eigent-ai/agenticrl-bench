#!/bin/bash

SERVICE_DIR="/opt/services/api-gateway"
LOG_DIR="$SERVICE_DIR/logs"
mkdir -p "$LOG_DIR"

echo "Starting ApiGateway with remote debugging on port 8200..."

java -Xdebug -Xrunjdwp:server=y,transport=dt_socket,address=8200, suspend=n -cp $SERVICE_DIR/classes com.example.ApiGateway > "$LOG_DIR/api-gateway.log" 2>&1 &

echo $! > "$SERVICE_DIR/pid"
echo "ApiGateway started with PID $(cat $SERVICE_DIR/pid)"
