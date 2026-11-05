#!/bin/bash
# Append a period to the end of the last line of each file argument.
# Files whose last line already ends with a period are skipped.
# Usage: append_period.sh file1.txt [file2.txt ...]

for f in "$@"; do
    [[ -f "$f" ]] || continue
    last_char=$(tail -c 1 "$f")
    [[ "$last_char" == "." ]] && continue
    vim -e -s -c 'normal Ga.' -c 'wq' "$f" 2>/dev/null
done
