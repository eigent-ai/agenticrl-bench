#!/bin/bash
set -e
java -cp /opt/csv-processor/bin com.example.CsvProcessor \
    /opt/csv-processor/input \
    /tmp/processing_report.properties
