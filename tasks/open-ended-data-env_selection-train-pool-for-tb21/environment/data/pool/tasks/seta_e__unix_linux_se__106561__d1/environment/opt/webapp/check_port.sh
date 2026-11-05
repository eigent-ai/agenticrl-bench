#!/bin/bash
PORT=${1:-9000}

OUTPUT=$(netstat -ln | grep ":${PORT} ")
if [ -z "$OUTPUT" ]; then
    echo "no process found on port ${PORT}" >&2
    exit 1
fi
echo "Port ${PORT} is in use"
