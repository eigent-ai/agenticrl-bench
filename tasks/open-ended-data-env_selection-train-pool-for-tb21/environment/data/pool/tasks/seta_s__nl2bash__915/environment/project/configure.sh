#!/bin/bash
# Configuration template processor
# Reads vars.conf and processes all .in template files

set -e

PROJ_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD_DIR="$PROJ_DIR/build"
VARS_FILE="$PROJ_DIR/vars.conf"

# Template file list
TEMPLATES=(
    "src/main/app.conf.in"
    "src/main/Makefile.in"
    "src/lib/config.h.in"
    "src/lib/Makefile.in"
    "version.txt.in"
    "tests/test.conf.in"
    "tests/Makefile.in"
)

# Parse vars.conf
declare -A VARS
while IFS= read -r line; do
    # Skip comments and empty lines
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    [[ -z "$line" ]] && continue
    key="${line%%=*}"
    value="${line#*=}"
    VARS["$key"]="$value"
done < "$VARS_FILE"

# Process templates
mkdir -p "$BUILD_DIR"

for tmpl in "${TEMPLATES[@]}"; do
    src="$PROJ_DIR/$tmpl"
    if [[ ! -f "$src" ]]; then
        echo "ERROR: Template not found: $src" >&2
        exit 1
    fi

    # Determine output path (strip .in suffix)
    rel_path="${tmpl%.in}"
    dest="$BUILD_DIR/$rel_path"
    mkdir -p "$(dirname "$dest")"

    # Substitute @VAR@ patterns
    cp "$src" "$dest"
    for key in "${!VARS[@]}"; do
        sed -i "s|@${key}@|${VARS[$key]}|g" "$dest"
    done
done

echo "Configuration complete. Processed ${#TEMPLATES[@]} templates."
