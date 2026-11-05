#!/bin/bash
set -e

echo "Starting worker service..."

# Load Redis secret from Docker secrets
source /run/secrets/redis

echo "Connecting to Redis at ${REDIS_HOST}..."
echo "Worker service initialized successfully"
