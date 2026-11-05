#!/bin/bash
# Log line counting utilities

count_lines() {
    local file="$1"
    local count
    count=$(cat -n "$file" | tail -n 1 | cut -f1 | xargs)
    echo "${count:-0}"
}
