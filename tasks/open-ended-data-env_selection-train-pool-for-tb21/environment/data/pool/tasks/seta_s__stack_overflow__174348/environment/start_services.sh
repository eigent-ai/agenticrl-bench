#!/bin/bash
# Start the Flask webapp in background
source /root/.local/bin/env 2>/dev/null || true
nohup /root/.local/bin/uv run --with flask python3 /opt/webapp/app.py > /var/log/webapp.log 2>&1 &

# Start nginx
nginx

# Wait for services to be ready
sleep 2
