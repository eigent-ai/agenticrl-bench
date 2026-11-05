#!/bin/bash
# Remove stale directories listed in the manifest

CONFIG_FILE="/opt/maintenance/config.ini"
source "$CONFIG_FILE"

manifest="$manifest_file"
logfile="$log_dir/cleanup.log"

for dir in $(cat "$manifest"); do
    full_path="$target_dir/$dir"
    if [ -d "$full_path" ] && [ -z "$(ls $full_path)" ]; then
        rmdir "$full_path"
        echo "REMOVED: $dir" > "$logfile"
    fi
done

echo "Cleanup complete."
