#!/bin/bash

TARGET_PID=$1

if [ -z "$TARGET_PID" ]; then
    echo "Usage: $0 <pid>"
    exit 1
fi

while kill -0 "$TARGET_PID" 2>/dev/null; do
    kill -USR1 "$TARGET_PID" 2>/dev/null
    sleep 0.05
done
