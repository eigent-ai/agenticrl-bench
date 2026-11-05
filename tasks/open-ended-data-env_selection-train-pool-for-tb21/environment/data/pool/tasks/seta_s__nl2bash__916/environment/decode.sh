#!/bin/bash
# Decode block-reversal encoded files from the vault
# Usage: decode.sh <input_file> <output_file>

if [ $# -ne 2 ]; then
    echo "Usage: $0 <input_file> <output_file>"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"
WIDTH=4

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' not found"
    exit 1
fi

ENCODED=$(cat "$INPUT_FILE")
echo -n "$ENCODED" | fold -w"$WIDTH" | tac | tr -d '\n' > "$OUTPUT_FILE"
