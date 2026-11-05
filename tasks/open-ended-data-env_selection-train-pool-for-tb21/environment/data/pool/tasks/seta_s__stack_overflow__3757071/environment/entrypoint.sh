#!/bin/bash
cd /app
python3 /app/server.py &
sleep 2
exec "$@"
