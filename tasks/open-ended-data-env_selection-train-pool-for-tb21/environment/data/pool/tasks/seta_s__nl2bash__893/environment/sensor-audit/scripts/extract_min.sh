#!/bin/bash
# Extract minimum value from column $2 of CSV file $1
datafile="$1"
col="$2"
cut -d',' -f"$col" "$datafile" | sort | head -n 1
