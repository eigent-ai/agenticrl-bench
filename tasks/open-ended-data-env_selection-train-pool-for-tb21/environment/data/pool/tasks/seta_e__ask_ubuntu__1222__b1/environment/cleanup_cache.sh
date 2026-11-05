#!/bin/bash
# Cache cleanup script for /var/cache/appdata/
# Archives old cache files and truncates them

CACHE_DIR="/var/cache/appdata"
ARCHIVE_DIR="/var/cache/appdata/archive"
DATE=$(date +%Y%m%d_%H%M%S)

# Create archive directory if it doesn't exist
mkdir -p "$ARCHIVE_DIR"

errors=0

# Process each cache file
for cachefile in "$CACHE_DIR"/*.dat; do
    if [ -f "$cachefile" ]; then
        filename=$(basename "$cachefile")
        # Copy current cache to archive
        if cp "$cachefile" "$ARCHIVE_DIR/${filename%.dat}_$DATE.dat" 2>&1; then
            # Truncate the cache file
            if truncate -s 0 "$cachefile" 2>&1; then
                echo "Cleaned: $filename"
            else
                echo "Error: Failed to truncate $filename" >&2
                errors=$((errors + 1))
            fi
        else
            echo "Error: Failed to archive $filename" >&2
            errors=$((errors + 1))
        fi
    fi
done

if [ $errors -gt 0 ]; then
    echo "Cache cleanup completed with $errors errors." >&2
    exit 1
fi

echo "Cache cleanup completed."
exit 0
