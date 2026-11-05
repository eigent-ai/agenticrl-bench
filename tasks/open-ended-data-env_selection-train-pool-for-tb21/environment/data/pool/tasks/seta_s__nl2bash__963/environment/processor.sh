#!/bin/bash
# Process cached df output into structured JSON report
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.ini"

INPUT_FILE="$CACHE_DIR/raw_df.txt"

if [ ! -f "$INPUT_FILE" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Cache file not found: $INPUT_FILE" >> "$LOG_FILE"
    exit 1
fi

mkdir -p "$(dirname "$REPORT_FILE")"

# Build JSON report
{
    echo '{'
    echo '  "timestamp": "'$(date -Iseconds)'",'
    echo '  "filesystems": ['

    first=true
    # Skip the header line, process filesystem entries
    tail -n +2 "$INPUT_FILE" | while IFS= read -r line; do
        # Skip empty lines
        [ -z "$(echo "$line" | tr -d '[:space:]')" ] && continue

        device=$(echo "$line" | awk '{print $1}')
        total=$(echo "$line" | awk '{print $2}')
        used=$(echo "$line" | awk '{print $3}')
        available=$(echo "$line" | awk '{print $4}')
        use_pct=$(echo "$line" | awk '{print $4}')
        mount=$(echo "$line" | awk '{print $6}')

        # Validate this looks like a data line (total should be numeric)
        [[ "$total" =~ ^[0-9]+$ ]] || continue

        if [ "$first" = true ]; then
            first=false
        else
            echo ','
        fi

        echo -n "    {\"mount\": \"$mount\", \"device\": \"$device\", \"total_kb\": $total, \"used_kb\": $used, \"available_kb\": $available, \"use_pct\": $use_pct}"
    done

    echo ''
    echo '  ]'
    echo '}'
} > "$REPORT_FILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Report generated: $REPORT_FILE" >> "$LOG_FILE"
