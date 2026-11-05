#!/bin/bash
set -e

cd /app

echo "Compiling Java sources..."
javac -d build src/DateUtils.java src/DateProcessor.java

echo "Running DateProcessor..."
java -cp build DateProcessor

echo "Done."
