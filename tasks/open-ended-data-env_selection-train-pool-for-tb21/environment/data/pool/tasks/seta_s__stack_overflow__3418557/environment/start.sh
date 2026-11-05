#!/bin/bash
service nginx start
cd /opt/webapp
/opt/webapp/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 2 --daemon app:app
sleep 1
