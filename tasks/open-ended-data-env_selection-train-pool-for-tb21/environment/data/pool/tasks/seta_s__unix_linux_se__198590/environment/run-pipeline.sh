#!/bin/bash
set -e

echo "Setting up pipeline mounts..."
mount -a

# Additional read-only mount for stage2 verification data
mount --bind -o ro /var/pipeline/data /opt/pipeline/stage2/verify

echo "Running pipeline stages..."
cd /opt/pipeline

echo "Stage 1: Configuration loading and input processing..."
python3 stage1/process.py

echo "Stage 2: Data transformation..."
python3 stage2/process.py

echo "Stage 3: Finalization..."
python3 stage3/finalize.py

echo "Pipeline complete. Output at /var/pipeline/output/result.txt"
