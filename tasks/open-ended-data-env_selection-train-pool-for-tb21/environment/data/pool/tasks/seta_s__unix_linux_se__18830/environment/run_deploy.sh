#!/bin/bash
set -e

echo "Starting deployment..."

echo "Syncing assets..."
sudo /opt/deploy/bin/sync_assets

echo "Restarting deploy-app service..."
sudo /usr/sbin/service deploy-app restart

echo "Recording deployment timestamp..."
date "+%Y-%m-%d %H:%M:%S" > /opt/deploy/.last_deploy

echo "Deployment completed successfully."
