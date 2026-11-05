#!/bin/bash
LOG_FILE="/var/log/dataproc/pipeline.log"
ERROR_LOG="/opt/dataproc/logs/errors.log"
tail -f "$LOG_FILE" | grep "WARN" >> "$ERROR_LOG"
