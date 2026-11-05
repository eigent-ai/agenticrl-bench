#!/bin/bash
# WebEngine Code Statistics Audit
# Generates line/word/byte counts for all source files.

OUTPUT="code_stats.txt"

echo "WebEngine Code Statistics Audit" > "$OUTPUT"
echo "================================" >> "$OUTPUT"
echo "" >> "$OUTPUT"

# Count all source files and append to report
wc $(find . -name '*.[h|c|cpp|php|cc]') >> "$OUTPUT"

echo "Audit complete. Report saved to $OUTPUT"
