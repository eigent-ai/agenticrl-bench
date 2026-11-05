#!/bin/bash
# Extract maximum value from column $2 of CSV file $1
datafile="$1"
col="$2"
cut -d',' -f"$col" "$datafile" | sort | tail -n 1
