#!/bin/bash
echo "=== Running Archive Pipeline ==="
echo "Step 1: Collecting file manifest..."
bash /opt/pipeline/scripts/collect.sh
echo "Step 2: Generating checksums..."
bash /opt/pipeline/scripts/checksum.sh
echo "Step 3: Creating backup..."
bash /opt/pipeline/scripts/backup.sh
echo "=== Pipeline Complete ==="
