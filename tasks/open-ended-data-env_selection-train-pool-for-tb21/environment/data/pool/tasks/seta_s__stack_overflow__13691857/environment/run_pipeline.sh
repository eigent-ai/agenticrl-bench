#!/bin/bash
echo "=== Step 1: Upscaling frames ==="
bash /opt/vidscaler/upscale.sh
echo "=== Step 2: Quality check ==="
python3 /opt/vidscaler/check_quality.py
