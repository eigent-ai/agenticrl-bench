#!/bin/bash
set -e
cd /opt/quarterutil
mkdir -p classes
javac -d classes src/QuarterUtils.java src/QuarterReport.java
echo "Compilation successful."
