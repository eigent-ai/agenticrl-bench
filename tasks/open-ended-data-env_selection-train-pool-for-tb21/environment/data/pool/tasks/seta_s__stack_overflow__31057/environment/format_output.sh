#!/bin/bash
# Post-processing script for report output
# Adds headers/footers and cleans up formatting

INPUT_FILE="$1"
OUTPUT_FILE="$2"

if [ -z "$INPUT_FILE" ] || [ -z "$OUTPUT_FILE" ]; then
    echo "Usage: format_output.sh <input_file> <output_file>"
    exit 1
fi

{
    echo "======================================"
    echo "  ASSESSMENT REPORT"
    echo "  Generated: $(date +%Y-%m-%d)"
    echo "======================================"
    echo ""

    # Clean up and output content
    sed 's/\\r//g' "$INPUT_FILE"

    echo ""
    echo "======================================"
    echo "  END OF REPORT"
    echo "======================================"
} > "$OUTPUT_FILE"
