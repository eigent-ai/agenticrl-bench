#!/bin/bash
# Remove temporary and junk files from the media library
source /srv/media/config/pipeline.conf

OUTPUT="/srv/media/reports/cleanup.log"
> "$OUTPUT"

# Find and remove junk files
for f in $(find ${media_dirs//:/ } -type f \( -name "*.tmp" -o -name ".DS_Store" -o -name "Thumbs.db" \)); do
    rm -f "$f" && echo "Removed: $f" >> "$OUTPUT"
done

echo "Cleanup complete: $(wc -l < "$OUTPUT") files removed"
