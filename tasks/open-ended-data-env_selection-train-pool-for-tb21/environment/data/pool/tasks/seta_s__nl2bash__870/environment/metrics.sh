#!/bin/bash
#
# Code Metrics Report Generator
# Generates a report of PHP source file line counts
#

REPORT_DIR="reports"

echo "Generating code metrics report..."

find . -name '*.php' | xargs wc -l | sort -n
