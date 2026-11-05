#!/bin/bash
# Script to run all services and generate logs

# Source application environment configuration
if [ -f /app/config/init_env.sh ]; then
    source /app/config/init_env.sh
fi

# Source service environment if available
if [ -f /app/config/service_env ]; then
    source /app/config/service_env
fi

echo "Running backend service..."
python3 /app/services/backend_service.py

echo "Running maintenance script..."
/app/services/maintenance.sh

echo "Running config validator..."
/app/services/config_validator.sh

echo "All services completed. Logs are in /var/log/app/"
