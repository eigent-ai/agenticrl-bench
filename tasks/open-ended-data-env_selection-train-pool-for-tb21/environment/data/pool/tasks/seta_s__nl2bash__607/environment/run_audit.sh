#!/bin/bash
# File Modification Audit Script v1.2
# Generates sorted report of file modification times

CONF="/opt/audit/audit.conf"
STORE="/srv/filestore"
OUTDIR="/opt/audit/report"

mkdir -p "$OUTDIR"

# Collect file data and generate report
ls -lR --time-style=long-iso "$STORE" | \
    grep "^-" | \
    awk '{print $6, $7, $NF}' | \
    sort -r > "$OUTDIR/file_report.txt"

echo "Audit complete. Report at $OUTDIR/file_report.txt"
