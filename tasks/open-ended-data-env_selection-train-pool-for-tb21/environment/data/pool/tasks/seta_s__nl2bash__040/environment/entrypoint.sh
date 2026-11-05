#!/bin/bash
python3 /opt/gitlab-api/api_server.py &
sleep 1
exec "$@"
