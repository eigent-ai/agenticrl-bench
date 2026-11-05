#!/bin/sh
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Validate environment
[[ -f "$SCRIPT_DIR/paths.conf" ]] || { echo "Missing paths.conf"; exit 1; }

echo "Starting system health check..."
"$SCRIPT_DIR/generate_report.sh"
echo "Report generated at $SCRIPT_DIR/reports/latest.json"
