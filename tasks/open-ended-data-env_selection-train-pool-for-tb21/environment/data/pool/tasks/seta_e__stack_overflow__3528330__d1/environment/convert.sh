#!/bin/bash
# Batch video converter
INPUT_DIR="/opt/mediaconv/input"
OUTPUT_DIR="/opt/mediaconv/output"

mkdir -p $OUTPUT_DIR

cd $INPUT_DIR

echo "Starting batch conversion..."

for i in *.flv *.mov *.avi; do
    echo "Converting $i..."
    ffmpeg -i $i $OUTPUT_DIR/$i.mp4
done

echo "Conversion complete."
