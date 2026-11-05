#!/bin/bash
./numcrunch data/input.csv > output.txt
exit_code=$?
if [ $exit_code -ne 0 ]; then
    echo "Error: numcrunch exited with code $exit_code" >&2
    exit $exit_code
fi
echo "Output written to output.txt"
