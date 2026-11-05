#!/bin/bash
SRC_DIR="${1:-/opt/inventory/data}"
DEST_DIR="${2:-/opt/inventory/output/normalized}"

mkdir -p "$DEST_DIR"

# Copy data files for processing
cp "$SRC_DIR/hardware.csv" "$DEST_DIR/hardware.csv"
cp "$SRC_DIR/network.csv" "$DEST_DIR/network.csv"
cp "$SRC_DIR/services.csv" "$DEST_DIR/services.csv"
