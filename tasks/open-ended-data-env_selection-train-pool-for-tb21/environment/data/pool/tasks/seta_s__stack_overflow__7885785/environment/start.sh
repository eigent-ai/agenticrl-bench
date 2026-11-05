#!/bin/bash
mkdir -p /home/user/extracted
python3 /opt/mtls-api/server.py &
sleep 2
exec "$@"
