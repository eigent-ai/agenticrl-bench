#!/bin/bash
# Main entry point: set up environment and generate config
cd /opt/webapp

# Load environment configuration
./scripts/setup_env.sh

# Generate application config
source ./scripts/app.sh
