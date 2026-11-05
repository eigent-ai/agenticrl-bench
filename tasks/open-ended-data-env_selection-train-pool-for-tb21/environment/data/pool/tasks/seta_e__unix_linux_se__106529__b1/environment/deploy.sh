#!/bin/bash
set -e

CONFIG_FILE="$HOME/.deploy/config.env"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "ERROR: deployment config not found at $CONFIG_FILE" >&2
    exit 2
fi

source "$CONFIG_FILE"

TIMESTAMP=$(date -Iseconds)
echo "${TIMESTAMP} [${DEPLOY_ENV}] ${APP_NAME}-${APP_VERSION} deployed by ${DOAS_USER:-unknown}" >> /var/log/deploy.log

echo "Deployed: ${APP_NAME} ${APP_VERSION} to ${DEPLOY_ENV}"
