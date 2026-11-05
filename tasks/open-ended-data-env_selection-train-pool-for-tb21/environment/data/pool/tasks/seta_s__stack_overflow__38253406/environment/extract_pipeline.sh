#!/bin/bash
set -e

BASEDIR="/project"
MANIFEST="$BASEDIR/manifest.json"
OUTDIR="$BASEDIR/output"

# Parse manifest
videos=$(grep -oP '"video":\s*"\K[^"]+' "$MANIFEST")
for video in $videos; do
    video_name=$(basename "$video" .mp4)
    frames_str=$(grep -A1 "$video" "$MANIFEST" | grep -oP '"frames":\s*\[\K[^\]]+')
    frames=$(echo "$frames_str" | tr -d ' ' | tr ',' '\n')

    # Build select expression
    select_expr=""
    for f in $frames; do
        if [ -z "$select_expr" ]; then
            select_expr="eq(n\,$f)"
        else
            select_expr="$select_expr,eq(n\,$f)"
        fi
    done

    echo "Extracting frames from $video: $select_expr"

    ffmpeg -i "$BASEDIR/$video" \
        -vf "select='$select_expr'" \
        "$OUTDIR/$video_name/frame%d.png" \
        -y 2>/tmp/ffmpeg_err.log

    echo "Done: $video_name"
done

echo "Pipeline complete."
