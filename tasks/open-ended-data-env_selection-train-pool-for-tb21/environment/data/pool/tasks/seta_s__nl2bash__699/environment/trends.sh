#!/bin/bash
set -e
TMPDIR="/var/lib/diskmon/tmp"
HISTORY="/var/lib/diskmon/history.dat"

if [ ! -f "$HISTORY" ]; then
    echo '{"avg_usage_7d": 0.0}' > "$TMPDIR/trends.json"
    exit 0
fi

# Calculate 7-day average usage
total=0
count=0
while IFS=',' read -r date usage; do
    total=$(echo "$total + $usage" | bc)
    count=$((count + 1))
done < "$HISTORY"

if [ $count -gt 0 ]; then
    avg=$(echo "scale=1; $total / $count" | bc)
else
    avg="0.0"
fi

echo "{\"avg_usage_7d\": $avg}" > "$TMPDIR/trends.json"
