#!/bin/bash
#
# Validation processor - checks that an INI file has valid key=value lines
#

SOURCE="$1"

if [ -z "$SOURCE" ]; then
    echo "Usage: validate.sh <ini_file>" >&2
    exit 1
fi

if [ ! -f "$SOURCE" ]; then
    echo "Source file not found: $SOURCE" >&2
    exit 1
fi

line_num=0
while IFS= read -r line; do
    line_num=$((line_num + 1))
    # Skip empty lines and comments
    [[ -z "$(echo "$line" | tr -d '[:space:]')" ]] && continue
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    [[ "$line" =~ ^[[:space:]]*\[ ]] && continue

    if ! echo "$line" | grep -q '='; then
        echo "Validation error at line $line_num: $line" >&2
        exit 1
    fi
done < "$SOURCE"

echo "Validation passed: $SOURCE"
exit 0
