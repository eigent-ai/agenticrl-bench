#!/bin/bash
target_size_mb=$1
target_size_bytes=$((target_size_mb * 1048576))
current_size=$(du -sb /var/log/journal 2>/dev/null | cut -f1)
if [ "$current_size" -gt "$target_size_bytes" ]; then
  for f in $(ls -t /var/log/journal/simulated/*.journal 2>/dev/null | tail -n +2); do
    rm -f "$f"
    current_size=$(du -sb /var/log/journal 2>/dev/null | cut -f1)
    if [ "$current_size" -le "$target_size_bytes" ]; then break; fi
  done
fi
echo "Vacuuming done, freed space."
