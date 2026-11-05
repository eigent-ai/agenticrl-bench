#!/bin/bash
# Validates a workspace token format
# Usage: validate.sh <token>
# Returns 0 if valid, 1 if invalid

TOKEN="$1"

if [ -z "$TOKEN" ]; then
    echo "Usage: validate.sh <token>"
    exit 1
fi

if [[ "$TOKEN" =~ ^[a-zA-Z0-9]{,32}$ ]]; then
    echo "Valid token: $TOKEN"
    exit 0
else
    echo "Invalid token: $TOKEN"
    exit 1
fi
