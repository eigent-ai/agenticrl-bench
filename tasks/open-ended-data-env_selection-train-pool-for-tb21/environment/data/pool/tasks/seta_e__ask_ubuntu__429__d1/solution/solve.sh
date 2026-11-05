#!/bin/bash
set -e

INCOMING="/backups/incoming"
EXTRACTED="/backups/extracted"
CONSOLIDATED="/backups/consolidated"
MANIFEST="/backups/manifest.json"
ERRORS="/backups/errors.log"

mkdir -p "$EXTRACTED" "$CONSOLIDATED"
> "$ERRORS"

# Function to extract an archive
extract_archive() {
    local archive="$1"
    local basename="$2"
    local format="$3"
    local dest="$EXTRACTED/$basename"
    mkdir -p "$dest"

    case "$format" in
        tar.gz)
            tar -xzf "$archive" -C "$dest" 2>>/tmp/extract_err.txt
            ;;
        gzip)
            local outname="${basename}"
            gunzip -c "$archive" > "$dest/$outname" 2>>/tmp/extract_err.txt
            ;;
        tar.bz2)
            tar -xjf "$archive" -C "$dest" 2>>/tmp/extract_err.txt
            ;;
        bzip2)
            local outname="${basename}"
            bunzip2 -c "$archive" > "$dest/$outname" 2>>/tmp/extract_err.txt
            ;;
        tar.xz)
            tar -xJf "$archive" -C "$dest" 2>>/tmp/extract_err.txt
            ;;
        xz)
            local outname="${basename}"
            xz -dc "$archive" > "$dest/$outname" 2>>/tmp/extract_err.txt
            ;;
    esac
}

# Determine format from filename
get_format() {
    local fname="$1"
    if [[ "$fname" == *.tar.gz ]]; then echo "tar.gz"
    elif [[ "$fname" == *.gz ]]; then echo "gzip"
    elif [[ "$fname" == *.tar.bz2 ]]; then echo "tar.bz2"
    elif [[ "$fname" == *.bz2 ]]; then echo "bzip2"
    elif [[ "$fname" == *.tar.xz ]]; then echo "tar.xz"
    elif [[ "$fname" == *.xz ]]; then echo "xz"
    fi
}

# Get base name without archive extension
get_basename() {
    local fname="$1"
    if [[ "$fname" == *.tar.gz ]]; then echo "${fname%.tar.gz}"
    elif [[ "$fname" == *.gz ]]; then echo "${fname%.gz}"
    elif [[ "$fname" == *.tar.bz2 ]]; then echo "${fname%.tar.bz2}"
    elif [[ "$fname" == *.bz2 ]]; then echo "${fname%.bz2}"
    elif [[ "$fname" == *.tar.xz ]]; then echo "${fname%.tar.xz}"
    elif [[ "$fname" == *.xz ]]; then echo "${fname%.xz}"
    fi
}

# Build manifest using Python for JSON safety
MANIFEST_ENTRIES=""

for archive_path in "$INCOMING"/*; do
    fname=$(basename "$archive_path")
    format=$(get_format "$fname")
    base=$(get_basename "$fname")

    if [ -z "$format" ]; then
        echo "$fname: unknown format, skipping" >> "$ERRORS"
        continue
    fi

    > /tmp/extract_err.txt
    if extract_archive "$archive_path" "$base" "$format"; then
        # Check if extraction actually produced files
        file_count=$(find "$EXTRACTED/$base" -type f | wc -l)
        if [ "$file_count" -eq 0 ]; then
            echo "$fname: extraction produced no files" >> "$ERRORS"
            rm -rf "$EXTRACTED/$base"
            continue
        fi
    else
        echo "$fname: extraction failed" >> "$ERRORS"
        rm -rf "$EXTRACTED/$base"
        continue
    fi

    # Check for errors in extraction
    if [ -s /tmp/extract_err.txt ]; then
        # tar errors indicate corruption
        if grep -qi "error\|corrupt\|invalid\|unexpected\|truncat" /tmp/extract_err.txt; then
            echo "$fname: extraction failed - $(cat /tmp/extract_err.txt)" >> "$ERRORS"
            rm -rf "$EXTRACTED/$base"
            continue
        fi
    fi
done

# Build manifest with Python
python3 << 'PYEOF'
import os
import json
import subprocess
import hashlib

EXTRACTED = "/backups/extracted"
manifest = []

for dirname in sorted(os.listdir(EXTRACTED)):
    dirpath = os.path.join(EXTRACTED, dirname)
    if not os.path.isdir(dirpath):
        continue

    # Determine original archive name and format
    format_map = {
        "config_backup": ("config_backup.tar.gz", "tar.gz"),
        "single_data": ("single_data.gz", "gzip"),
        "logs_backup": ("logs_backup.tar.bz2", "tar.bz2"),
        "report": ("report.bz2", "bzip2"),
        "database_backup": ("database_backup.tar.xz", "tar.xz"),
        "compressed": ("compressed.xz", "xz"),
        "application_data": ("application_data.tar.gz", "tar.gz"),
    }

    if dirname not in format_map:
        continue

    archive_name, detected_format = format_map[dirname]

    # Get file list (relative paths)
    files = []
    for root, dirs, fnames in os.walk(dirpath):
        for f in fnames:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, dirpath)
            files.append(rel)
    files.sort()

    # Compute MD5 checksums
    checksums = {}
    for rel in files:
        full = os.path.join(dirpath, rel)
        result = subprocess.run(["md5sum", full], capture_output=True, text=True)
        md5hash = result.stdout.split()[0]
        checksums[rel] = md5hash

    # Get total size
    result = subprocess.run(["du", "-sb", dirpath], capture_output=True, text=True)
    total_size = int(result.stdout.split()[0])

    manifest.append({
        "archive": archive_name,
        "detected_format": detected_format,
        "files": files,
        "checksums": checksums,
        "total_size": total_size
    })

with open("/backups/manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print(f"Manifest created with {len(manifest)} entries")
PYEOF

# Part 3: Consolidate archives
for dirname in "$EXTRACTED"/*/; do
    base=$(basename "$dirname")
    file_count=$(find "$dirname" -type f | wc -l)

    if [ "$file_count" -gt 1 ]; then
        # Multi-file: tar.xz
        outfile="$CONSOLIDATED/${base}.tar.xz"
        tar -cJf "$outfile" -C "$EXTRACTED" "$base"
        sha256sum "$outfile" | awk '{print $1}' > "${outfile}.sha256"
    elif [ "$file_count" -eq 1 ]; then
        # Single file: xz
        single_file=$(find "$dirname" -type f | head -1)
        outfile="$CONSOLIDATED/${base}.xz"
        xz -c "$single_file" > "$outfile"
        sha256sum "$outfile" | awk '{print $1}' > "${outfile}.sha256"
    fi
done

echo "Consolidation complete"
ls -la "$CONSOLIDATED"
echo "Done!"
