#!/bin/bash

apply_gamma_settings() {
    local output_file="$1"

    echo "" >> "$output_file"
    echo "# Gamma settings" >> "$output_file"

    for ((i=1; i<MONITOR_COUNT; i++)); do
        local gamma="${MONITOR_GAMMAS[$i]}"
        local output="${MONITOR_OUTPUTS[$i]}"

        if [[ -n "$gamma" ]]; then
            echo "xrandr --output $output --gamma $gamma" >> "$output_file"
        fi
    done
}
