#!/bin/bash
TMUX_SESSION="data_pipeline"
OUTPUT_FILE="/opt/monitor/output/session_log.txt"

tmux capture-pane -t "${TMUX_SESSION}" -p > "$OUTPUT_FILE"
echo "Capture complete. Output written to $OUTPUT_FILE"
