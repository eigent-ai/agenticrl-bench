#!/bin/bash
# collect.sh - Collect files from a data directory and output a manifest

DATA_DIR=$1

if [ -z "$DATA_DIR" ]; then
    echo "Usage: collect.sh <data_directory>" >&2
    exit 1
fi

if [ ! -d "$DATA_DIR" ]; then
    echo "Error: $DATA_DIR is not a directory" >&2
    exit 1
fi

FILES=`find $DATA_DIR -type f`

for f in $FILES; do
    printf '%s\0' "$f"
done
