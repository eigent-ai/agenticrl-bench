#!/bin/bash
# Log file parsing utilities

count_errors() {
    local file="$1"
    awk '{print $5}' "$file" | grep -c "ERROR"
}
