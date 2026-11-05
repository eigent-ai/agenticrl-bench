#!/bin/bash
# Review processed output with syntax highlighting via less
# Requires source-highlight package

if [ -z "$1" ]; then
    echo "Usage: $0 <file>"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Error: File not found: $1"
    exit 1
fi

export LESSOPEN="| /usr/lib/source-highlight/src-hilite-lesspipe.sh %s"

less "$1"
