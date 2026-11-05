#!/bin/bash
OUTPUT_FILE="${1:-/opt/sandbox/output/result.txt}"
echo "=== Sandbox Demo ==="
echo "User: $(whoami)"
echo "UID: $(id -u)"
echo "GID: $(id -g)"
echo "Groups: $(id -Gn)"
echo "Hostname: $(hostname)"
echo "Date: $(date)"

mkdir -p "$(dirname "$OUTPUT_FILE")"
{
    echo "user=$(whoami)"
    echo "uid=$(id -u)"
    echo "gid=$(id -g)"
    echo "groups=$(id -Gn)"
    echo "hostname=$(hostname)"
    echo "date=$(date)"
    echo "status=success"
} > "$OUTPUT_FILE"

echo "Output written to $OUTPUT_FILE"
