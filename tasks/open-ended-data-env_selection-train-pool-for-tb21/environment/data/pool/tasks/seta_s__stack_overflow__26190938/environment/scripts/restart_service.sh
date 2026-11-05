#!/bin/bash
SERVICE=$1
PORT=$2
PASSWORD=$3

echo "Authenticating with database for $SERVICE..."
echo "Restarting $SERVICE on port $PORT..."
sleep 0.1
echo "Service $SERVICE restarted successfully"
