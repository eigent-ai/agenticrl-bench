#!/bin/bash
# Filter manifest by file extensions
# Usage: filter.sh ext1 ext2 ...
MANIFEST="/opt/inventory/output/manifest.csv"

if [ $# -eq 0 ]; then
    echo "Usage: filter.sh ext1 [ext2 ...]"
    exit 1
fi

# Build pattern
pattern="*.$1"
shift
for ext in "$@"; do
    pattern="$pattern|*.$ext"
done

echo "filepath,size,md5"
tail -n +2 "$MANIFEST" | grep "$pattern"
