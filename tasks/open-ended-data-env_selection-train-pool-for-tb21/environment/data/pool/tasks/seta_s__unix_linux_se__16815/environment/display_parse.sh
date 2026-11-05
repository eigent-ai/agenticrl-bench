#!/bin/bash
# Display parsing and validation library for DSM
# Handles X11 DISPLAY string validation and component extraction

# Validate a DISPLAY string
# Valid formats: [host]:display[.screen]
# Returns 0 if valid, 1 if invalid
validate_display() {
    local display_str="$1"

    if [ -z "$display_str" ]; then
        return 1
    fi

    # Check DISPLAY format
    if [[ "$display_str" =~ ^:[0-9]+$ ]]; then
        return 0
    fi

    return 1
}

# Parse a DISPLAY string into components
# Outputs: HOST=<host> DISPLAY_NUM=<num> SCREEN=<screen>
parse_display() {
    local display_str="$1"

    validate_display "$display_str"
    if [ $? -ne 0 ]; then
        echo "Error: Invalid DISPLAY string: $display_str"
        return 1
    fi

    local host
    local display_num
    local screen

    # Split on colon to get host and remainder
    host=$(echo "$display_str" | cut -d: -f1)
    local remainder
    remainder=$(echo "$display_str" | cut -d: -f2)

    if [ -z "$host" ]; then
        echo "Error: Empty host component"
        return 1
    fi

    # Split remainder on dot to get display and screen
    display_num=$(echo "$remainder" | cut -d. -f1)
    if echo "$remainder" | grep -q '\.'; then
        screen=$(echo "$remainder" | cut -d. -f2)
    else
        screen=""
    fi

    echo "HOST=$host"
    echo "DISPLAY_NUM=$display_num"
    echo "SCREEN=$screen"
    return 0
}
