#!/bin/bash
set -e
if [ ! -d bin ] || [ -z "$(ls -A bin 2>/dev/null)" ]; then
    echo "No compiled classes found. Run ./compile.sh first."
    exit 1
fi
java -cp bin Main data/students.csv output.csv
