#!/bin/bash
BASEDIR="/opt/medialib"
CONFIG="$BASEDIR/config"
SOURCES="$BASEDIR/sources"
OUTPUT="$BASEDIR/output/discovered.txt"

EXCLUDE_PATTERN=$(grep '^exclude=' "$CONFIG/sources.conf" | cut -d= -f2)

> "$OUTPUT"

# Primary search: iterate configured formats
while IFS= read -r ext; do
    [[ "$ext" =~ ^#.*$ ]] && continue
    [[ -z "$ext" ]] && continue
    find "$SOURCES" -type f -not -path '*/.*' -not -path "$EXCLUDE_PATTERN" -name "*.$ext" >> "$OUTPUT"
done < "$CONFIG/formats.conf"

# Secondary comprehensive regex scan
find "$SOURCES" -type f -not -path '*/.*' -not -path "$EXCLUDE_PATTERN" \
    -regex ".*\\\\.(jpg|jpeg|gif|png)" >> "$OUTPUT"

echo "Discovered $(wc -l < "$OUTPUT") files"
