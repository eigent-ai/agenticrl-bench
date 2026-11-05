#!/bin/bash
if [ -z "$1" ]; then
    echo "Usage: trace_access.sh <command> [args...]"
    exit 1
fi
strace -e trace=network "$@" 2>&1 | grep -oP '"\K[^"]+' | sort -u
