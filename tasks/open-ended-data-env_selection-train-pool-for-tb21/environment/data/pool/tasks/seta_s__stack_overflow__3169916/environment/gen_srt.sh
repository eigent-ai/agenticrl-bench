#!/bin/bash
INPUT="$1"
OUTPUT="$2"
START_TC="$3"
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$INPUT")
SECONDS=$(printf "%.0f" "$DURATION")

IFS=':' read -r sh sm ss sf <<< "$START_TC"
START_SECS=$(( 10#$sh * 3600 + 10#$sm * 60 + 10#$ss ))

> "$OUTPUT"
for i in $(seq 0 $((SECONDS - 1))); do
    s=$i
    e=$((i + 1))
    printf "%d\n" "$i"  >> "$OUTPUT"
    printf "%02d:%02d:%02d.000 --> %02d:%02d:%02d.000\n" \
        $((s/3600)) $(((s%3600)/60)) $((s%60)) \
        $((e/3600)) $(((e%3600)/60)) $((e%60)) >> "$OUTPUT"
    printf "%02d:%02d:%02d:%02d\n\n" \
        $(((s + START_SECS)/3600)) $((((s + START_SECS)%3600)/60)) $(((s + START_SECS)%60)) 0 >> "$OUTPUT"
done
