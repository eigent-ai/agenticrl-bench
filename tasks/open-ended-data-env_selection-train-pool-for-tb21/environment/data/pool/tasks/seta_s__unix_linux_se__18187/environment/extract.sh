#!/bin/bash
# Usage: extract.sh <php_file> <line_number> <output_file>
FILE="$1"
LINE="$2"
export OUTPUT_FILE="$3"
vim -E -s -u NONE +"$LINE" -S /opt/block_extractor/extract.vim "$FILE" 2>/dev/null
