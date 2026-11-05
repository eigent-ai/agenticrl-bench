#!/bin/bash
set -e

XML_FILE="$1"
ARCHIVE_DIR="/srv/archive"

if [[ -z "$XML_FILE" ]] || [[ ! -f "$XML_FILE" ]]; then
    echo "process.sh: cannot open file: '${XML_FILE}'" >&2
    exit 1
fi

TITLE=$(grep -o '<title>[^<]*</title>' "$XML_FILE" | sed 's/<[^>]*>//g' | head -1)
[[ -z "$TITLE" ]] && TITLE="(no title)"
BASENAME=$(basename "$XML_FILE")
TIMESTAMP=$(date -Iseconds)

echo "${TIMESTAMP},${BASENAME},${TITLE}" >> "${ARCHIVE_DIR}/report.log"
mv "$XML_FILE" "${ARCHIVE_DIR}/${BASENAME}"
