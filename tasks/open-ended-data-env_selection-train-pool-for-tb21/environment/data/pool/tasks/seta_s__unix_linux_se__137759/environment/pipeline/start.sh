#!/bin/bash
LOG_DIR="/opt/pipeline/logs"
mkdir -p "$LOG_DIR"
exec /opt/pipeline/worker.sh
