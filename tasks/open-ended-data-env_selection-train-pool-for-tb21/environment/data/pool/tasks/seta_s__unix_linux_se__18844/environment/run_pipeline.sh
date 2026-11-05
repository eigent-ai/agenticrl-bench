#!/bin/bash
set -e
source /opt/dataproc/config.ini
mkdir -p "$LOG_DIR"
echo "[$(date)] Pipeline $PIPELINE_NAME starting" >> "$LOG_DIR/pipeline.log"
bash /opt/dataproc/extract.sh
echo "[$(date)] Extract complete" >> "$LOG_DIR/pipeline.log"
python3 /opt/dataproc/transform.py
echo "[$(date)] Transform complete" >> "$LOG_DIR/pipeline.log"
bash /opt/dataproc/load.sh
echo "[$(date)] Load complete" >> "$LOG_DIR/pipeline.log"
echo "[$(date)] Pipeline $PIPELINE_NAME finished" >> "$LOG_DIR/pipeline.log"
