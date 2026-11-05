#!/bin/bash
# Generate module paths for the build pipeline
BASE_DIR="$HOME/code"
MODULE_PATH=$(find "$BASE_DIR" -type d -name '[^.]*' | tr '\n' ':')
echo "MODULE_PATH=$MODULE_PATH" > /opt/workspace/modules.env
echo "Module paths generated successfully."
