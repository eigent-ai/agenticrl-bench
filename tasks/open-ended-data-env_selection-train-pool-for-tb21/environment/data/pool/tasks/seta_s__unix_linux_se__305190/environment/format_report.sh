#!/bin/bash

INPUT="/opt/monitor/raw_metrics.txt"
OUTPUT="/opt/monitor/report.txt"

awk 'NR==1{next} {
    cpu = substr($2, 1, length($2))
    mem = $3
    printf "%d> %s %s %s\n", NR-1, $1, cpu, mem
}' "$INPUT" > "$OUTPUT"
