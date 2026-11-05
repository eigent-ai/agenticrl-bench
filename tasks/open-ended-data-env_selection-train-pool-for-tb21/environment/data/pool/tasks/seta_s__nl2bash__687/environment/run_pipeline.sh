#!/bin/bash
set -e
cd "$(dirname "$0")"
echo "=== Pipeline Started ==="
echo "Step 1: Preprocessing..."
./scripts/preprocess.sh
echo "Step 2: Transforming..."
./scripts/transform.py
echo "Step 3: Validating..."
./scripts/validate.sh
echo "=== Pipeline Complete ==="
