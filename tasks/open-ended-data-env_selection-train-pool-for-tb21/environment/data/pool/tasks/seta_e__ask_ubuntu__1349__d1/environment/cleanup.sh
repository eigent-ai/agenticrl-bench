#!/bin/bash
# Simulated cleanup script
echo "Running cleanup at $(date)"
if [[ "$1" == "--fail" ]]; then
    echo "ERROR: Cleanup failed!"
    exit 1
fi
echo "Cleanup completed successfully"
exit 0
