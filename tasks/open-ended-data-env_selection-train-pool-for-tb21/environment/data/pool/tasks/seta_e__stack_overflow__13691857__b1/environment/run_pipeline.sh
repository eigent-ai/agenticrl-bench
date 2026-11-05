#!/bin/bash
echo "=== Step 1: Resampling clips ==="
bash /opt/audioscaler/resample.sh
echo "=== Step 2: Quality check ==="
python3 /opt/audioscaler/check_quality.py
