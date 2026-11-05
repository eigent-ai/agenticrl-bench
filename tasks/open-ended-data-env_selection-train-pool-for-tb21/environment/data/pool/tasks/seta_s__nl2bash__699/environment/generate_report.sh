#!/bin/bash
set -e

BASEDIR="/opt/diskmon"
OUTDIR="/var/lib/diskmon/reports"
TMPDIR="/var/lib/diskmon/tmp"

mkdir -p "$OUTDIR" "$TMPDIR"

# Step 1: Collect mount and usage data
"$BASEDIR/collect.sh"

# Step 2: Parse and filter
"$BASEDIR/parse.sh"

# Step 3: Calculate trends
"$BASEDIR/trends.sh"

# Step 4: Generate JSON report
"$BASEDIR/format_json.sh"

echo "Report generated at $OUTDIR/latest.json"
