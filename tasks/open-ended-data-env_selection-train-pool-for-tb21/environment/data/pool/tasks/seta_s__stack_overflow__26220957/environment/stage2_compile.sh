#!/bin/bash
set -e

STAGE_DIR="$1"

echo "Starting compilation stage..."

cd /app
make compile

echo "Compilation completed."
ls -la "$STAGE_DIR/"
