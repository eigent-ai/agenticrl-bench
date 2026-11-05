#!/bin/bash
# Parse a single log entry into CSV format: timestamp,severity,message
# Usage: parse_entry.sh "<log_line>"

LINE="$1"

# Extract fields from standard log format
echo "$LINE" | sed -E 's/^\[([^]]+)\] ([A-Z]+): (.*)$/\1,\2,\3/'
