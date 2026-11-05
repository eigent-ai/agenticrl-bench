#!/bin/bash
# Summarize the log data
awk -F"\t" "{sum+=\$5; count++} END {print \"Total entries: \" count; print \"Total bytes: \" sum}" /app/output/filtered.txt > /app/output/summary.txt
