#!/bin/bash
outdir=$1
cd "$outdir"
if [ -f - ]; then
    rm -
fi
