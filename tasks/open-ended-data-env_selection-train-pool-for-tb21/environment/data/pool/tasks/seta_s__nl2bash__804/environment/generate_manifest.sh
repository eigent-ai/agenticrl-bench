#!/bin/bash
# Generate a depth-sorted manifest of all directories under the target

CONFIG_FILE="/opt/maintenance/config.ini"
source "$CONFIG_FILE"

# Find all directories, sort by depth, and extract paths
find "$target_dir" -type d -printf '%P\t%d\n' | sort -nk1 | cut -f1 > "$manifest_file"

echo "Manifest generated: $manifest_file"
