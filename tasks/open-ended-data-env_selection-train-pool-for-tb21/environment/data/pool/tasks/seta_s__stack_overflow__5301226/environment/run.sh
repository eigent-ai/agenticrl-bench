#!/bin/bash
cd /app
mkdir -p output build
javac -d build src/*.java
if [ $? -ne 0 ]; then
    echo "Compilation failed"
    exit 1
fi
java -cp build EventDateNormalizer
