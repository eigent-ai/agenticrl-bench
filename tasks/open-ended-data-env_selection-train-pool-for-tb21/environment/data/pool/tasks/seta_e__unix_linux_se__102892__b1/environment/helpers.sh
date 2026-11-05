#!/usr/bin/env bash
# Shell utility functions for data processing


sanitize_input() {
    echo "$1" | tr -d '[:cntrl:]' | tr '[:upper:]' '[:lower:]'
}


retry_command() {
    local retries="${1:-3}"
    shift
    local n=0
    while [ "$n" -lt "$retries" ]; do
        "$@" && return 0
        n=$((n + 1))
    done
    return 1
}


log_message() {
    local level="${1:-INFO}"
    printf "[%s] [%s] %s\n" "$(date '+%Y-%m-%d %H:%M:%S')" "$level" "$2"
}
