#!/bin/bash
cd /app
mkdir -p build
javac -Xlint:unchecked -d build src/*.java
if [ $? -ne 0 ]; then
    echo "Compilation failed!"
    exit 1
fi
java -cp build ReportGenerator
