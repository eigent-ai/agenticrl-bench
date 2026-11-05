#!/bin/bash
# Generate .def.out marker files for processed definitions
# Updated: 2024-01-15

cd /workspace/project

echo "Generating definition markers..."

# Find all .def files and create corresponding .out markers
find ./src/core ./src/codegen ./plugins/auth -name '*.def' | sed 's/\(.*\)/\1.out/' | xargs touch

echo "Done. Marker generation complete."
