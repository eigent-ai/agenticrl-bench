#!/bin/bash
# Shared helper: format and log test results
PROJECT=$1
STATUS=$2
TIMESTAMP=$3

REPORT_FILE="/var/log/testing/results_summary.log"
echo "[$TIMESTAMP] Project: $PROJECT | Status: $STATUS" >> "$REPORT_FILE"
