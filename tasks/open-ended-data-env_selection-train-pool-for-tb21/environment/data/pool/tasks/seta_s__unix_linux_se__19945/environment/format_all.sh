#!/bin/bash
# Format all source files using Vim auto-indent

echo "Formatting source files..."

for f in src/*; do
    echo "Processing $f..."
    vim -c "norm gg=G" "$f"
done

echo "Done formatting."
