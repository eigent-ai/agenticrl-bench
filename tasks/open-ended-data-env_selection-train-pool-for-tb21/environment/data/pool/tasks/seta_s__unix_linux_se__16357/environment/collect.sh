#!/bin/bash
datadir=$1
outfile=$2
> "$outfile"
cd "$datadir"
for file in $(ls); do
    cat $file >> "$outfile"
done
