#!/bin/bash

MONITOR_NAMES=()
MONITOR_OUTPUTS=()
MONITOR_RESOLUTIONS=()
MONITOR_POSITIONS=()
MONITOR_GAMMAS=()
MONITOR_TEMPS=()
MONITOR_CUSTOM=()
MONITOR_COUNT=0

parse_monitors() {
    local config_file="$1"
    local idx=0

    while read -r line; do
        [[ "$line" =~ ^#.*$ ]] && continue
        [[ -z "$line" ]] && continue

        read -r name output resolution position gamma temp custom <<< "$line"

        MONITOR_NAMES[$idx]="$name"
        MONITOR_OUTPUTS[$idx]="$output"
        MONITOR_RESOLUTIONS[$idx]="$resolution"
        MONITOR_POSITIONS[$idx]="$position"
        MONITOR_GAMMAS[$idx]="$gamma"
        MONITOR_TEMPS[$idx]="$temp"
        MONITOR_CUSTOM[$idx]="$custom"

        idx=$((idx + 1))
    done < "$config_file"

    MONITOR_COUNT=$idx
}
