#!/bin/bash
# Check status of running screen-based jobs

OUTPUT=$(screen -ls)
ACTIVE=$(echo "$OUTPUT" | grep "(Attached)" | wc -l)
DETACHED=$(echo "$OUTPUT" | grep "(Detached)" | wc -l)

echo "=== Job Status Report ==="
echo "Active (attached): $ACTIVE"
echo "Detached (running): $DETACHED"
echo ""
echo "Session details:"
echo "$OUTPUT" | grep -E "\t" | while read line; do
    SESSION=$(echo "$line" | awk '{print $1}')
    STATUS=$(echo "$line" | awk '{print $2}')
    echo "  $SESSION - $STATUS"
done
