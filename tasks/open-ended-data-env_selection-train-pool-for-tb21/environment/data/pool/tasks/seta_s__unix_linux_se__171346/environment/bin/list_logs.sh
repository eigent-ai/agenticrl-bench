#!/bin/bash
# Lists .log files in a directory with their line counts.
# Usage: list_logs.sh <directory>
DIR=$1

for logfile in $DIR/*.log; do
    [ -f $logfile ] && echo "$(wc -l < $logfile) $logfile"
done
