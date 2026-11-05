#!/bin/bash
# Generate master HLS playlist from profiles.conf

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROFILES_CONF="$SCRIPT_DIR/profiles.conf"
OUTPUT_DIR="$SCRIPT_DIR/output"
MASTER_PLAYLIST="$OUTPUT_DIR/master.m3u8"

echo "#EXTM3U" > "$MASTER_PLAYLIST"
echo "#EXT-X-VERSION:3" >> "$MASTER_PLAYLIST"

current_profile=""
declare -A prof_width prof_height prof_bitrate

while IFS= read -r line; do
    line="$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
    [[ -z "$line" || "$line" == \#* ]] && continue

    if [[ "$line" =~ ^\[(.+)\]$ ]]; then
        current_profile="${BASH_REMATCH[1]}"
        continue
    fi

    if [[ "$line" =~ ^([^=]+)=(.+)$ ]]; then
        key="${BASH_REMATCH[1]}"
        value="${BASH_REMATCH[2]}"
        case "$key" in
            width) prof_width[$current_profile]="$value" ;;
            height) prof_height[$current_profile]="$value" ;;
            bitrate) prof_bitrate[$current_profile]="$value" ;;
        esac
    fi
done < "$PROFILES_CONF"

for profile in "${!prof_bitrate[@]}"; do
    BITRATE="${prof_bitrate[$profile]}"
    WIDTH="${prof_width[$profile]}"
    HEIGHT="${prof_height[$profile]}"
    RESOLUTION="${WIDTH}x${HEIGHT}"

    echo "#EXT-X-STREAM-INF:BANDWIDTH=${BITRATE},RESOLUTION=${RESOLUTION}" >> "$MASTER_PLAYLIST"
    echo "${profile}/playlist.m3u8" >> "$MASTER_PLAYLIST"
done

echo "Master playlist generated at $MASTER_PLAYLIST"
