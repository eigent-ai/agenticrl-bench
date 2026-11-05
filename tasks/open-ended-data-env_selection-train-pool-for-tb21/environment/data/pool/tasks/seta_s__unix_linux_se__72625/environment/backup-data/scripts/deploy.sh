#!/bin/bash
# Deployment helper script

set -euo pipefail

TARGET="${1:-/var/www/app}"
RELEASE_TAG="${2:-latest}"

echo "Deploying release: $RELEASE_TAG to $TARGET"

if [[ ! -d "$TARGET" ]]; then
    echo "Error: target directory $TARGET does not exist"
    exit 1
fi

rsync -a --checksum ./dist/ "$TARGET/"
echo "Deploy complete: $RELEASE_TAG"
