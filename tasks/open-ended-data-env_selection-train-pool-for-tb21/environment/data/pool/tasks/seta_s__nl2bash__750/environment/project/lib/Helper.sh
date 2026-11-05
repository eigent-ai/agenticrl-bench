#!/bin/bash
# Helper utilities - updated version

helper_greet() {
    echo "Hello from helper.sh (v2)"
}

helper_validate() {
    if [ -z "$1" ]; then
        echo "Error: no argument provided" >&2
        return 1
    fi
    echo "Valid: $1"
    return 0
}

helper_cleanup() {
    echo "Cleaning up temporary files..."
    rm -f /tmp/project_*.tmp
}
