#!/bin/bash
set -e
CONFIG=/opt/vidscaler/config.json
read_cfg() { python3 -c "import json; d=json.load(open('${CONFIG}')); print(d['$1'])"; }

INPUT_DIR=$(read_cfg input_dir)
OUTPUT_DIR=$(read_cfg output_dir)
WIDTH=$(read_cfg output_width)
HEIGHT=$(read_cfg output_height)
FILTER=$(read_cfg scale_filter)

mkdir -p "$OUTPUT_DIR"
count=0
for input_file in "$INPUT_DIR"/*.png; do
    filename=$(basename "$input_file")
    ffmpeg -y -i "$input_file" \
        -vf "scale=${WIDTH}:${HEIGHT}:flags=${FILTER}" \
        -frames:v 1 \
        "$OUTPUT_DIR/$filename" 2>/dev/null
    count=$((count + 1))
done
echo "Upscaling complete: $count frame(s) written to $OUTPUT_DIR"
