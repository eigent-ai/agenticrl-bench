#!/bin/bash
# Safe file writing — only create files that don't already exist

safe_write() {
    local filepath="$1"
    local content="$2"
    if [ -f "$filepath" ]; then
        echo "$content" > "$filepath"
    fi
}
