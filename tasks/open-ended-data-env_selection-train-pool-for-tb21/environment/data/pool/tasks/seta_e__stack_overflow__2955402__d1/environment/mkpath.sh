#!/bin/bash
# Directory creation utility

ensure_dir() {
    local target="$1"
    if [ ! -d "$target" ]; then
        mkdir "$target"
    fi
}
