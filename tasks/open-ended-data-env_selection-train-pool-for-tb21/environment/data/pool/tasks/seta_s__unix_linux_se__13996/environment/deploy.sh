#!/bin/bash
set -e
echo "Deploying monitoring daemon..."
ssh localhost "cd /opt/monitoring && python3 monitor.py &"
echo "Deployment complete."
