#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONF_FILE="$SCRIPT_DIR/fixtures.conf"
OUTPUT_DIR="$SCRIPT_DIR/output"

mkdir -p "$OUTPUT_DIR"

count=0

cat "$CONF_FILE" | while read -r line; do
    [ -z "$line" ] && continue

    size_spec=$(echo "$line" | awk '{print $NF}')
    filename=$(echo "$line" | sed "s/[[:space:]]*${size_spec}[[:space:]]*$//")

    echo "Creating fixture: '$filename' with size $size_spec"

    if echo "$size_spec" | grep -qiE '^[0-9]+[kmg]$'; then
        numeric=$(echo "$size_spec" | grep -oE '^[0-9]+')
        suffix=$(echo "$size_spec" | grep -oiE '[kmg]$' | tr '[:upper:]' '[:lower:]')
        dd if=/dev/zero of="$OUTPUT_DIR/$filename" bs=1${suffix} count=${numeric} 2>/dev/null
    else
        dd if=/dev/zero of="$OUTPUT_DIR/$filename" bs=${size_spec} count=1 2>/dev/null
    fi

    count=$((count + 1))
done

echo "Generated $count fixture files."

if [ "$count" -eq 0 ]; then
    echo "ERROR: No fixtures were generated!"
    exit 1
fi

exit 0
