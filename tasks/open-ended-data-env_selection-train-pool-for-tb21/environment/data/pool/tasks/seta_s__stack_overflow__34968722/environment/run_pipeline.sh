#!/bin/bash
set -e

cd /app
python pipeline.py

if [ $? -eq 0 ]; then
    echo "Pipeline completed successfully."
else
    echo "Pipeline failed with exit code $?." >&2
    exit 1
fi
