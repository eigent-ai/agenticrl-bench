#!/bin/bash
cd /app
: > extraction_report.txt
for a in *.tar.*; do
    d=${a%%.tar.*}; mkdir -p "$d"; tar -xf "$a" -C "$d"
    echo "$a tar -xf -> $d" >> extraction_report.txt
done
echo "archive4 archive5 skipped (unzip / 7z)" >> extraction_report.txt
