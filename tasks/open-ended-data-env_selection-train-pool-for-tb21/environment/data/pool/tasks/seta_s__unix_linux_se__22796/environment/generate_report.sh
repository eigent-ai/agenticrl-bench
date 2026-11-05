#!/bin/bash

log_message "INFO" "Starting report generation"

input="${OUTPUT_DIR}/processed.csv"
report="${OUTPUT_DIR}/report.txt"

validate_input "$input" || exit 1

line_count=$(wc -l < "$input")
total=$(awk -F',' '{sum += $3} END {print sum}' "$input")

{
    echo "Pipeline Report"
    echo "==============="
    echo "Records processed: $line_count"
    echo "Total value: $total"
} > "$report"

log_message "INFO" "Report generated: $report"
