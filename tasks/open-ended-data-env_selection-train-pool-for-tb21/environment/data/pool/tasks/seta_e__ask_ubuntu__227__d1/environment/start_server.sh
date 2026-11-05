#!/bin/bash
python3 /server/auth_server.py > /tmp/server.log 2>&1 &
echo $! > /tmp/server.pid
sleep 1
