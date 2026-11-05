#!/bin/bash
set -e
echo "=== Building dataproc ==="
make clean
make all OUTDIR="${OUTDIR}"
echo "=== Build complete ==="
