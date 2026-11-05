#!/bin/bash
# Content-type mismatch checker
# Verifies that file content matches its stated extension

FILEPATH=$1

if [ -z "$FILEPATH" ] || [ ! -f "$FILEPATH" ]; then
    echo "skip"
    exit 0
fi

# Get extension from filename
FILENAME=$(basename "$FILEPATH")
EXT=$(echo "$FILENAME" | sed 's/.*\.//' | tr '[:upper:]' '[:lower:]')

# Expected MIME types by extension
declare -A EXPECTED_MIME
EXPECTED_MIME[txt]="text/plain"
EXPECTED_MIME[json]="text/json"
EXPECTED_MIME[xml]="text/xml"
EXPECTED_MIME[png]="image/png"
EXPECTED_MIME[jpg]="image/jpeg"
EXPECTED_MIME[jpeg]="image/jpeg"
EXPECTED_MIME[gif]="image/gif"
EXPECTED_MIME[pdf]="application/pdf"

# Only check if we have a mapping for this extension
EXPECTED="${EXPECTED_MIME[$EXT]}"
if [ -z "$EXPECTED" ]; then
    echo "skip"
    exit 0
fi

# Get actual content type from file magic
ACTUAL=$(file --mime-type -b "$FILEPATH")

if [ "$EXPECTED" != "$ACTUAL" ]; then
    echo "mismatch"
else
    echo "match"
fi
