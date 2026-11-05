#!/usr/bin/env bash
# Deployment configuration and helpers

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/helpers.sh"


DEFAULT_HOST="localhost"
DEFAULT_PORT="8080"
DEFAULT_DEBUG="false"
DEFAULT_WORKERS="4"
DEFAULT_LOG_LEVEL="warn"


deploy_service() {
    local config_file="$1"
    if [ ! -f "$config_file" ]; then
        echo "Error: Config not found: $config_file" >&2
        return 1
    fi
    local host="${DEFAULT_HOST}"
    local port="${DEFAULT_PORT}"
    while IFS='=' read -r key val; do
        [[ "$key" =~ ^[[:space:]]*# ]] && continue
        [ -n "$key" ] && eval "local ${key}=${val}"
    done < "$config_file"
    echo "Deploying to ${host}:${port}"
}
