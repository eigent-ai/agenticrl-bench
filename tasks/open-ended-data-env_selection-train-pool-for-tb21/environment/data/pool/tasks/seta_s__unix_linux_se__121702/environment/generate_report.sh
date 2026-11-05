#!/bin/bash
set -e

BASEDIR="/opt/sysinventory"
OUTDIR="$BASEDIR/output"
COLLECTORS="$BASEDIR/collectors"

mkdir -p "$OUTDIR"

echo "Running system inventory collectors..."

bash "$COLLECTORS/cpu_info.sh" > "$OUTDIR/cpu_info.out"
bash "$COLLECTORS/memory_info.sh" > "$OUTDIR/memory_info.out"
bash "$COLLECTORS/filesystems.sh" > "$OUTDIR/filesystems.out"
bash "$COLLECTORS/block_devices.sh" > "$OUTDIR/block_devices.out"
bash "$COLLECTORS/kernel_params.sh" > "$OUTDIR/kernel_params.out"

echo "Aggregating results..."

python3 "$BASEDIR/aggregate.py"

echo "Report generated at $BASEDIR/report.json"
