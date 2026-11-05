#!/bin/bash
# Usage: check_port.sh <port>
# Prints the PID of the process listening on <port>, or exits 1 if none.
PORT=${1:-9000}

OUTPUT=$(netstat -ln | grep ":${PORT} ")
if [ -z "$OUTPUT" ]; then
    echo "no process found on port ${PORT}" >&2
    exit 1
fi
echo "Port ${PORT} is in use"
