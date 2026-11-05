#!/bin/bash
# Compare parsed mount data against expected mount specification
# Usage: compare_mounts.sh <parsed_file> <spec_file> <server_name>

parsed_file="$1"
spec_file="$2"
server_name="$3"

if [ ! -f "$parsed_file" ] || [ ! -f "$spec_file" ]; then
    echo "Error: Input files not found" >&2
    exit 1
fi

# Filter out virtual filesystems - skip non-physical mounts
filtered_parsed=$(grep -v "tmpfs\|overlay\|sysfs\|proc\|devtmpfs\|devpts" "$parsed_file")

# Check each expected mount against actual mounts
while IFS='|' read -r exp_mount exp_fstype exp_options; do
    [ -z "$exp_mount" ] && continue
    [[ "$exp_mount" == \#* ]] && continue

    # Search for mount point in parsed data
    match=$(echo "$filtered_parsed" | grep "|${exp_mount}|")

    if [ -z "$match" ]; then
        echo "${server_name}|${exp_mount}|${exp_fstype}|missing||${exp_options}"
    else
        actual_options=$(echo "$match" | cut -d'|' -f4)
        actual_fstype=$(echo "$match" | cut -d'|' -f3)

        # Verify all required options are present
        all_present=true
        IFS=',' read -ra req_opts <<< "$exp_options"
        for opt in "${req_opts[@]}"; do
            if ! echo "$actual_options" | grep -qw "$opt"; then
                all_present=false
                break
            fi
        done

        if [ "$all_present" = true ]; then
            echo "${server_name}|${exp_mount}|${exp_fstype}|compliant|${actual_options}|${exp_options}"
        else
            echo "${server_name}|${exp_mount}|${exp_fstype}|misconfigured|${actual_options}|${exp_options}"
        fi
    fi
done < "$spec_file"

# Identify unexpected mounts (present in system but not in spec)
while IFS='|' read -r device mountpoint fstype options; do
    [ -z "$mountpoint" ] && continue
    if ! grep -q "^${mountpoint}|" "$spec_file"; then
        echo "${server_name}|${mountpoint}|${fstype}|unexpected|${options}|"
    fi
done <<< "$filtered_parsed"
