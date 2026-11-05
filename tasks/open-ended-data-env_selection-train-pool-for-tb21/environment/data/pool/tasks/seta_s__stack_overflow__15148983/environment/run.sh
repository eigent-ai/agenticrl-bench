#!/bin/bash
cd /opt/pipeline
timeout 60 python3 process_flights.py
exit_code=$?
if [ $exit_code -eq 124 ]; then
    echo "ERROR: Pipeline timed out after 60 seconds"
    exit 124
elif [ $exit_code -ne 0 ]; then
    echo "ERROR: Pipeline failed with exit code $exit_code"
    exit $exit_code
fi
echo "Pipeline completed successfully"
exit 0
