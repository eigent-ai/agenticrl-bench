#!/bin/bash
# Parse CPU count from a server's proc_cpuinfo snapshot
SNAPSHOT_DIR="$1"
grep processor "$SNAPSHOT_DIR/proc_cpuinfo" | wc -l
