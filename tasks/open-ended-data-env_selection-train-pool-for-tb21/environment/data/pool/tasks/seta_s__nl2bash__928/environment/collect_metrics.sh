#!/bin/bash
source /opt/monitor/config.conf
OUTPUT_FILE="${METRICS_DIR}/raw_metrics.txt"
mkdir -p "${METRICS_DIR}"
echo "# JBoss Process Metrics - $(date '+%Y-%m-%d %H:%M:%S')" > "$OUTPUT_FILE"
echo "# Format: PID VSZ_KB COMMAND" >> "$OUTPUT_FILE"
ps axu | grep jboss | cut -d' ' -f2,5,11- >> "$OUTPUT_FILE"
LINE_COUNT=$(grep -cv "^#" "$OUTPUT_FILE")
echo "INFO: Collected metrics for $LINE_COUNT processes"
