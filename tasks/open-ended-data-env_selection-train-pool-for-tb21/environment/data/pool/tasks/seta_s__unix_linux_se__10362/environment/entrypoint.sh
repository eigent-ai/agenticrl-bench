#!/bin/bash
set -e
python3 /opt/app/server.py &
sleep 1
exec "$@"
