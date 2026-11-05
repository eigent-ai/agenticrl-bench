#!/bin/bash
set -e
cd /app
if [ ! -f ./pipeline ]; then
    echo "No compiled binary found. Run ./build.sh first."
    exit 1
fi
./pipeline data/sales.csv output.csv
