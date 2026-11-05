#!/bin/bash
export TZ=America/Chicago
cd /app
mkdir -p output build
javac -d build src/*.java
java -cp build EventNormalizer
