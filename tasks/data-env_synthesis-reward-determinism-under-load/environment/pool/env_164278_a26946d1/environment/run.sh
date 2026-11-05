#!/bin/bash
cd /opt/eventcal
mkdir -p output build
javac -d build src/*.java 2>&1
if [ $? -ne 0 ]; then
    echo "Compilation failed" >&2
    exit 1
fi
java -cp build Main
