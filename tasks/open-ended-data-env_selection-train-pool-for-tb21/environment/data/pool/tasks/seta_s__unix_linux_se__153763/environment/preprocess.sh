#!/bin/bash
# Preprocess raw data: strip comments and blank lines, normalize whitespace
input="$1"
output="$2"
if [ -z "$input" ] || [ -z "$output" ]; then
    echo "Usage: preprocess.sh <input> <output>" >&2
    exit 1
fi
sed '/^#/d; /^$/d; s/[[:space:]]\+/,/g' "$input" > "$output"
