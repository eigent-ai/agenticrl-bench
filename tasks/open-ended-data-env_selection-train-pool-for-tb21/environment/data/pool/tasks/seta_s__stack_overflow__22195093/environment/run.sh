#!/bin/bash
cd /opt/taskctl
mkdir -p build output
javac -d build src/*.java
if [ $? -ne 0 ]; then
    echo "Build failed!"
    exit 1
fi
java -cp build TaskCtl 2025-04-01 /opt/taskctl/tasks.csv
