#!/bin/bash
# parse_records.sh - Parse structured records from a source file into JSON
# Usage: bash parse_records.sh <source_file>

SOURCE_FILE="$1"

if [ -z "$SOURCE_FILE" ] || [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: Source file not found: $SOURCE_FILE" >&2
    exit 1
fi

IN_RECORD=0
FIRST_RECORD=1

echo "["

while IFS= read -r line; do
    line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

    [ -z "$line" ] && continue
    echo "$line" | grep -q "^#" && continue

    if [ "$line" = "BEGIN_RECORD" ]; then
        IN_RECORD=1
        if [ $FIRST_RECORD -eq 0 ]; then
            echo ","
        fi
        FIRST_RECORD=0
        echo -n "  {"
        FIRST_FIELD=1
        continue
    fi

    if [ "$line" = "END_RECORD" ]; then
        IN_RECORD=0
        echo -n "}"
        continue
    fi

    if [ $IN_RECORD -eq 1 ]; then
        FIELD_NAME=$(echo "$line" | cut -d':' -f1 | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        FIELD_VALUE=$(echo "$line" | cut -d':' -f2 | sed 's/;[[:space:]]*$//;s/^[[:space:]]*//;s/[[:space:]]*$//')

        if [ $FIRST_FIELD -eq 0 ]; then
            echo -n ", "
        fi
        FIRST_FIELD=0

        FIELD_VALUE=$(echo "$FIELD_VALUE" | sed 's/"/\\"/g')
        echo -n "\"$FIELD_NAME\": \"$FIELD_VALUE\""
    fi
done < "$SOURCE_FILE"

echo ""
echo "]"
