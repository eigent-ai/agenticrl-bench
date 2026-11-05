#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
source /opt/services/debug.env
mkdir -p "$DIR/logs"

java -agentlib:jwdp=transport=dt_socket,server=y,suspend=n,address=*:${AUTH_DEBUG_PORT} \
    -cp "$DIR/classes" AuthService \
    > "$DIR/logs/stdout.log" 2> "$DIR/logs/stderr.log" &

echo $! > "$DIR/service.pid"
echo "auth-service started with PID $!"
