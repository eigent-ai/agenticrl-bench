#!/bin/bash
# Deploy environment configuration

echo "Loading deploy environment..."

export DEPLOY_ROOT="/opt/deploy"
export APP_VERSION="3.2.1"
export RELEASE_DIR="/home/deploy/releases"
export LOG_DIR="/var/log/deploy"
export MAX_RELEASES=10

echo "Environment ready."
