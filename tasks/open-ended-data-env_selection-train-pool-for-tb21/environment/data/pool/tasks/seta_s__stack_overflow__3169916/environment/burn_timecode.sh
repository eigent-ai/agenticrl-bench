#!/bin/bash
INPUT="$1"
OUTPUT="$2"
ffmpeg -y -i "$INPUT" -vf "drawtext=text='timecode':fontsize=28:fontcolor=white:x=10:y=10" -c:v libx264 "$OUTPUT"
