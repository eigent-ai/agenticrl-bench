#!/bin/bash
# Application config generator
# Reads environment variables and writes config file

OUTPUT_DIR="/opt/webapp/output"
CONFIG_FILE="$OUTPUT_DIR/app.conf"

mkdir -p "$OUTPUT_DIR"

cat > "$CONFIG_FILE" <<CONF
DB_HOST=${DB_HOST:-}
DB_PORT=${DB_PORT:-}
DB_NAME=${DB_NAME:-}
APP_DATA_DIR=${APP_DATA_DIR:-}
APP_SECRET_KEY=${APP_SECRET_KEY:-}
APP_SESSION_TOKEN=${APP_SESSION_TOKEN:-}
LOG_FORMAT=${LOG_FORMAT:-}
LOG_DIR=${LOG_DIR:-}
CONF
