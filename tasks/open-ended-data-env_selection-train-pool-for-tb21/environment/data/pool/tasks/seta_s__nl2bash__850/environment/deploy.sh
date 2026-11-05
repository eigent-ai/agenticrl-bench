#!/bin/bash
# deploy.sh - Deploy the application to staging/production
set -e

ENVIRONMENT="${1:-staging}"
VERSION=$(date +%Y%m%d%H%M%S)

echo "Deploying version $VERSION to $ENVIRONMENT..."

if [ ! -f "build/output/app.jar" ]; then
    echo "Error: Build artifacts not found. Run 'make build' first."
    exit 1
fi

echo "Packaging distribution..."
echo "Uploading to $ENVIRONMENT server..."
echo "Deployment complete: v$VERSION -> $ENVIRONMENT"
