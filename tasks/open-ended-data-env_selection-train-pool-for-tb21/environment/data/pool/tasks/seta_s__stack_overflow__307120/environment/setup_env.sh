#!/bin/bash
# Orchestrator: load all configuration sources

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Load database configuration
./scripts/db_config.sh

# Load application configuration
./scripts/app_config.sh

# Load secrets
./scripts/gen_secrets.sh

# Load utility functions and set log config
source "$SCRIPT_DIR/utils.sh"
set_log_config
