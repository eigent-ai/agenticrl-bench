#!/bin/bash
set -e
mkdir -p /opt/csv-processor/bin
javac -d /opt/csv-processor/bin \
    /opt/csv-processor/src/com/example/TempWorkspace.java \
    /opt/csv-processor/src/com/example/CsvProcessor.java
