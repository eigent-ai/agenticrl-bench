#!/bin/bash
set -e
echo "Starting pipeline..."
python3 /app/pipeline/processor.py
python3 /app/pipeline/archiver.py
echo "Pipeline completed at $(date -u +%Y-%m-%dT%H:%M:%SZ)" > /app/state/done.txt
echo "Done."
