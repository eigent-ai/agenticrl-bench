#!/bin/bash

source /etc/log-cleanup.conf

echo "=== File Summary Report ==="
echo "Directory: $LOG_DIR"
echo ""

ALLFILES=$(find $LOG_DIR -exec grep -l '.' {} \; 2>/dev/null)

for ext in log csv tmp gz pid lock; do
    count=$(echo $ALLFILES | grep -c "\.$ext")
    echo "  .$ext: $count files"
done

echo ""
echo "=== End Report ==="
