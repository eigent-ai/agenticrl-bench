#!/bin/bash

# Build initramfs image for PXE netboot
# Usage: ./build_initramfs.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INITRAMFS_ROOT="$SCRIPT_DIR/initramfs_root"
OUTPUT_DIR="$SCRIPT_DIR/output"
CONFIG_DIR="$SCRIPT_DIR/config"

echo "=== Building initramfs image ==="

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

echo "Collecting files from $INITRAMFS_ROOT..."

# Create cpio archive from initramfs root
cd "$INITRAMFS_ROOT"
find . | cpio -o -H odc > "$OUTPUT_DIR/initrd.img"

echo "Build complete: $OUTPUT_DIR/initrd.img"
echo "Image size: $(du -h "$OUTPUT_DIR/initrd.img" | cut -f1)"
