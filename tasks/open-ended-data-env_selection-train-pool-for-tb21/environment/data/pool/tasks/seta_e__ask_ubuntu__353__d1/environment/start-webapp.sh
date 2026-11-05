#!/bin/bash
cd /opt/webapp
python3 app.py &
echo $! > /tmp/webapp.pid
