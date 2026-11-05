#!/bin/bash
WEBAPP_DIR="/opt/webapp"
APP_PORT=9000

if netstat -ln | grep -q ":${APP_PORT} "; then
    echo "ERROR: Port ${APP_PORT} is already in use. Cannot start webapp." >&2
    exit 1
fi

cd "$WEBAPP_DIR"
nohup python3 app.py > /var/log/webapp.log 2>&1 &
echo $! > /var/run/webapp.pid
echo "Webapp started on port ${APP_PORT} (PID $(cat /var/run/webapp.pid))"
