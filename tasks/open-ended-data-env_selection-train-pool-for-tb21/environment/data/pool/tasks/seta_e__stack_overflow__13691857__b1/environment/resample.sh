#!/bin/bash
set -e
CONFIG=/opt/audioscaler/config.json
read_cfg() { python3 -c "import json; d=json.load(open('${CONFIG}')); print(d['$1'])"; }

INPUT_DIR=$(read_cfg input_dir)
OUTPUT_DIR=$(read_cfg output_dir)
RATE=$(read_cfg output_sample_rate)
QUALITY=$(read_cfg resample_quality)

# Map quality name to sox rate effect flag
case "$QUALITY" in
    quick)     QFLAG="-q" ;;
    low)       QFLAG="-l" ;;
    medium)    QFLAG="-m" ;;
    high)      QFLAG="-h" ;;
    very-high) QFLAG="-v" ;;
    *)         QFLAG="-h" ;;
esac

mkdir -p "$OUTPUT_DIR"
count=0
for input_file in "$INPUT_DIR"/*.wav; do
    filename=$(basename "$input_file")
    sox "$input_file" "$OUTPUT_DIR/$filename" rate $QFLAG $RATE
    count=$((count + 1))
done
echo "Resampling complete: $count clip(s) written to $OUTPUT_DIR"
