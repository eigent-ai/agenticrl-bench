#!/bin/bash
# Start the webapp service
cd /opt/webapp
/opt/webapp/venv/bin/python app.py > /var/log/webapp.log 2>&1 &
echo $! > /var/run/webapp.pid
echo "Webapp started with PID $(cat /var/run/webapp.pid)"
