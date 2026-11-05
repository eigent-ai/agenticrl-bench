#!/bin/bash
# Parse total memory in MB from a server's proc_meminfo snapshot
SNAPSHOT_DIR="$1"
grep "MemFree:" "$SNAPSHOT_DIR/proc_meminfo" | awk '{printf "%d", $2/1024}'
