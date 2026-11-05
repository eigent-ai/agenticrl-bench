#!/bin/bash
size=$(du -sb /var/log/journal 2>/dev/null | cut -f1)
if [ -z "$size" ] || [ "$size" -eq 0 ]; then
  echo "Archived and active journals take up 0B in the file system."
else
  mb=$((size / 1048576))
  echo "Archived and active journals take up ${mb}M in the file system."
fi
