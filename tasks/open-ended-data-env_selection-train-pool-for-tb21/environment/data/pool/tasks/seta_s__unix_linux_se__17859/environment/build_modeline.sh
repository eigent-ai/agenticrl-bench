#!/bin/bash

generate_modelines() {
    local output_file="$1"

    for ((i=0; i<MONITOR_COUNT; i++)); do
        if [[ "${MONITOR_CUSTOM[$i]}" == "yes" ]]; then
            local res="${MONITOR_RESOLUTIONS[$i]}"
            local width="${res%x*}"
            local height="${res#*x}"
            local output="${MONITOR_OUTPUTS[$i]}"

            local cvt_output
            cvt_output=$(/usr/local/bin/cvt "$width" "$height" 60 2>/dev/null)

            local modeline
            modeline=$(echo "$cvt_output" | grep "^Modeline")

            local raw_name
            raw_name=$(echo "$modeline" | awk '{print $2}' | tr -d '"')
            mode_name=$(echo "$raw_name" | cut -d'_' -f1)

            local mode_params
            mode_params=$(echo "$modeline" | sed 's/^Modeline[[:space:]]*"[^"]*"[[:space:]]*//')

            echo "xrandr --newmode \"${mode_name}\" ${mode_params}" >> "$output_file"
            echo "xrandr --addmode ${output} \"${mode_name}\"" >> "$output_file"
            echo "xrandr --output ${output} --mode \"${mode_name}\" --pos ${MONITOR_POSITIONS[$i]}" >> "$output_file"
        else
            echo "xrandr --output ${MONITOR_OUTPUTS[$i]} --mode ${MONITOR_RESOLUTIONS[$i]} --pos ${MONITOR_POSITIONS[$i]}" >> "$output_file"
        fi
    done
}
