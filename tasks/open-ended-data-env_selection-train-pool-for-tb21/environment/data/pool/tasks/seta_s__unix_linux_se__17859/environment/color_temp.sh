#!/bin/bash

generate_color_temp() {
    local output_file="$1"

    echo "" >> "$output_file"
    echo "# Color temperature settings" >> "$output_file"

    for ((i=0; i<MONITOR_COUNT; i++)); do
        local temp="${MONITOR_TEMPS[$i]}"
        local output="${MONITOR_OUTPUTS[$i]}"

        if [[ -n "$temp" && "$temp" != "6500" ]]; then
            echo "redshift -m randr:output=$output -t $temp" >> "$output_file"
        fi
    done
}
