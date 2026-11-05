#!/bin/bash
# Counts log entries that contain a given pattern.
# Usage: count_entries.sh <logfile> <pattern>
LOGFILE=$1
PATTERN=$2

awk -v pat=$PATTERN 'index($0, pat) > 0 {n++} END {print n+0}' $LOGFILE
