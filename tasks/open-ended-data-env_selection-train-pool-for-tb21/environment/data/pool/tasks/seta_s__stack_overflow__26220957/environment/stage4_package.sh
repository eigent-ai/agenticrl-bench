#!/bin/bash
set -e

STAGE_DIR="$1"

echo "Starting packaging stage..."

cd /app
make package

echo "Packaging completed."
echo "Output artifacts:"
ls -la /app/build/output/
