#!/bin/bash
cd /opt/taskctl
mkdir -p build output
make
if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi
./build/taskctl 2025-04-01 /opt/taskctl/tasks.csv
