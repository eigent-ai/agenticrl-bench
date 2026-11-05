#!/bin/bash
# Common utility functions for the log sampling pipeline

log_info() {
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') $1"
}

log_error() {
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') $1" >&2
}

check_file_exists() {
    if [ ! -f "$1" ]; then
        log_error "File not found: $1"
        return 1
    fi
}

count_lines() {
    wc -l < "$1" | tr -d ' '
}

trim_whitespace() {
    echo "$1" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'
}
