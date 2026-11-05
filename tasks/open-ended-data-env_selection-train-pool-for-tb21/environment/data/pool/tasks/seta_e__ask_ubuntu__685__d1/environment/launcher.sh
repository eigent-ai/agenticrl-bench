#!/bin/bash
# DataSync Pro Launcher Script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JAR_FILE="$SCRIPT_DIR/datasync-pro.jar"
java -jar "$JAR_FILE" "$@"
