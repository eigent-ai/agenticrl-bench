#!/bin/bash
LOG_DIR="/opt/pipeline/logs"
mkdir -p "$LOG_DIR"
nohup /opt/pipeline/step1.sh && /opt/pipeline/step2.sh > "$LOG_DIR/batch.log" 2>&1 &
echo "Batch started"
