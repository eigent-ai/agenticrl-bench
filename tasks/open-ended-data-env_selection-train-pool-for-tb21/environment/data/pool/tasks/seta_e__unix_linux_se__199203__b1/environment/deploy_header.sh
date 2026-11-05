#!/bin/bash
# Deployment script for MyApp
# Auto-generated — do not edit manually
set -euo pipefail

APP_NAME="MyApp"
DEPLOY_DIR="/opt/myapp"
BACKUP_DIR="/opt/myapp/backups"
LOG_FILE="/var/log/myapp/deploy.log"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
