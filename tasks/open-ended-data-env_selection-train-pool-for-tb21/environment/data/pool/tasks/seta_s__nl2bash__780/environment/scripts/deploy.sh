#!/bin/bash
# Deployment script - runs audit before deploying
echo "=== Pre-deployment Configuration Audit ==="
bash /opt/deploy/scripts/audit.sh
if [[ $? -ne 0 ]]; then
    echo "ERROR: Audit failed. Aborting deployment."
    exit 1
fi
echo "Audit passed. Proceeding with deployment..."
