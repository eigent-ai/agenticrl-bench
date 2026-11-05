#!/bin/bash
set -e
cd /app
python pipeline.py
echo "Pipeline finished with exit code $?"
