#!/bin/bash
CONFIG="/opt/checker/thresholds.conf"
OUTPUT="/opt/checker/report/staleness_report.json"
mkdir -p "$(dirname "$OUTPUT")"
NOW=$(date +%s)

while IFS=: read -r app_name app_dir threshold; do
    [[ "$app_name" =~ ^# ]] && continue
    [[ -z "$app_name" ]] && continue

    result=$(find "$app_dir" -maxdepth 1 -type f -printf '%A@ %p\n' | sort -n | tail -1)

    latest_file=$(echo "$result" | awk '{print $2}')
    latest_epoch=$(echo "$result" | awk '{print $1}')

    hours_ago=$(( (NOW - ${latest_epoch%.*}) / 3600 ))

    if [ "$hours_ago" -gt "$threshold" ]; then
        stale="true"
    else
        stale="false"
    fi

    echo "{\"app\": \"$app_name\", \"latest_file\": \"$latest_file\", \"modified_epoch\": ${latest_epoch%.*}, \"hours_since_modified\": $hours_ago, \"threshold_hours\": $threshold, \"stale\": $stale},"
done < "$CONFIG" > "$OUTPUT"
