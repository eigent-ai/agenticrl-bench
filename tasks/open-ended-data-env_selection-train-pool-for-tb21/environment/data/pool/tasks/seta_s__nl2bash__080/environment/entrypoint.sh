#!/bin/bash
# Start the mock Grafana API server in the background
python3 /opt/grafana-mock/server.py &
# Keep container alive
exec sleep infinity
