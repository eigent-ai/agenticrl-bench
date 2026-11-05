#!/bin/bash
# Composite a green-screen foreground clip onto a background video.
set -e

FG="clips/green_clip.mp4"
BG="backgrounds/bg_blue.mp4"
OUTPUT="output/result.mp4"

mkdir -p output

ffmpeg -i "$FG" -i "$BG" \
  -filter_complex '[1:v]colorkey=0x00FF00:0.0:0.0[ckout];[0:v][ckout]overlay[out]' \
  -map '[out]' \
  -c:v libx264 \
  -pix_fmt yuv420p \
  -y "$OUTPUT"

echo "Done: $OUTPUT"
