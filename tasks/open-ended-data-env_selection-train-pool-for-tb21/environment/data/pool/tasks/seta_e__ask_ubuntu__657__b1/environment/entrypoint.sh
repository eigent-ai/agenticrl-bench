#!/bin/bash
# Start the backend server
python3 /opt/backend/server.py &
# Start nginx
nginx
# Keep container running
exec sleep infinity
