#!/bin/bash
set -e
BASEDIR=$(dirname "$0")
cd "$BASEDIR"

java -cp "dist/loganalyzer.jar:lib/*" LogAnalyzer -i data/access.log -o output/report.txt
echo "Processing complete. Report written to output/report.txt"
