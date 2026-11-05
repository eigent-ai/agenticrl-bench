#!/bin/bash
# Find files with identical content by comparing MD5 checksums
source /srv/media/config/pipeline.conf

OUTPUT="/srv/media/reports/duplicates.txt"
> "$OUTPUT"

# Compute checksums for all media files
find ${media_dirs//:/ } -type f -not -name "*.tmp" -not -name ".DS_Store" -not -name "Thumbs.db" | \
    xargs md5sum 2>/dev/null | sort > /tmp/all_checksums.txt

# Extract checksums that appear more than once
awk '{print $1}' /tmp/all_checksums.txt | sort | uniq -d > /tmp/dup_hashes.txt

# List all files with duplicate checksums
while IFS= read -r hash; do
    grep "^${hash}" /tmp/all_checksums.txt >> "$OUTPUT"
done < /tmp/dup_hashes.txt

count=$(wc -l < "$OUTPUT" 2>/dev/null || echo 0)
echo "Found $count files involved in duplicates"
