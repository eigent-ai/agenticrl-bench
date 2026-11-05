#!/bin/bash

echo "Packaging application..."
mkdir -p /app/ci/dist
cp /app/ci/build/app /app/ci/dist/app
chmod +x /app/ci/dist/app
echo "Application packaged to /app/ci/dist/app"
