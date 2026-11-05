#!/bin/bash
# Helper functions for virtual monitor setup

parse_resolution() {
    local res="$1"
    WIDTH="${res%x*}"
    HEIGHT="${res#*x}"
}

parse_position() {
    local pos="$1"
    POS_X="${pos%x*}"
    POS_Y="${pos#*x}"
}

parse_cvt_modeline() {
    local width="$1"
    local height="$2"
    local cvt_output
    cvt_output=$(cvt "$width" "$height" 60 2>/dev/null)
    MODELINE_NAME=$(echo "$cvt_output" | grep "Modeline" | awk '{print $2}')
    MODELINE_PARAMS=$(echo "$cvt_output" | grep "Modeline" | awk '{print $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12}')
}

format_clip_region() {
    local w="$1"
    local h="$2"
    local x="$3"
    local y="$4"
    echo "${w}+${h}+${x}+${y}"
}

calculate_total_geometry() {
    local max_right=0
    local max_bottom=0
    for config in "$@"; do
        IFS='|' read -r name res pos output vnc <<< "$config"
        parse_resolution "$res"
        parse_position "$pos"
        local right=$((POS_X + WIDTH))
        local bottom=$((POS_Y + HEIGHT))
        if [ "$right" -gt "$max_right" ]; then
            max_right=$right
        fi
        if [ "$bottom" -gt "$max_bottom" ]; then
            max_bottom=$bottom
        fi
    done
    TOTAL_WIDTH=$max_right
    TOTAL_HEIGHT=$max_bottom
}
