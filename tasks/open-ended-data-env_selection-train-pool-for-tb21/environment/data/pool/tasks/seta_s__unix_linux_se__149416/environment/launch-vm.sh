#!/bin/bash
# Generates the QEMU command and records it to the log directory.
set -euo pipefail

LOG_DIR=/var/log/vm-manager
mkdir -p "$LOG_DIR"
/opt/vm-manager/bin/generate-cmd.sh "$@" | tee "$LOG_DIR/last-cmd.log"
