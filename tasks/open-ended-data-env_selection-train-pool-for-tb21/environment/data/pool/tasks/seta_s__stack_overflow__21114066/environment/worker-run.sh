#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$DIR/logs"

java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005 \
    -cp "$DIR/classes" WorkerService \
    > "$DIR/logs/stdout.log" 2> "$DIR/logs/stderr.log" &

echo $! > "$DIR/service.pid"
echo "worker-service started with PID $!"
