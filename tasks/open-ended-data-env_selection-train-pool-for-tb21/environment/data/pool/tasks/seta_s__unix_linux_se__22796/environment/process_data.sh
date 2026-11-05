#!/bin/bash

log_message "INFO" "Starting data processing"

input_file="${DATA_DIR}/input.csv"
output_file="${OUTPUT_DIR}/processed.csv"

validate_input "$input_file" || exit 1

mkdir -p "$(dirname "$output_file")"
awk -F',' 'NR > 1 { print $1 "," $2 "," ($3 * 1.1) }' "$input_file" > "$output_file"

log_message "INFO" "Processing complete. Output: $output_file"
