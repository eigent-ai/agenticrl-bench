#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

mkdir -p "$BASE_DIR/output"

echo "Generating server report..."
python3 "$SCRIPT_DIR/generate_server_report.py"

echo "Generating metrics report..."
python3 "$SCRIPT_DIR/generate_metrics_report.py"

echo "Merging reports..."
python3 "$SCRIPT_DIR/merge_reports.py"

echo "Pipeline complete. Output in $BASE_DIR/output/"
