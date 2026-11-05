#!/bin/bash
# Utility: load environment files in the correct precedence order
# Loading order: global.env -> group envs (sorted) -> service envs (sorted)
# Later definitions override earlier ones

CONFIG_DIR="${1:-/opt/deploy/config}"

echo "Loading order:"
echo "  1. $CONFIG_DIR/global.env"
for f in $(find "$CONFIG_DIR/groups" -name "*.env" -type f 2>/dev/null | sort); do
    echo "  2. $f (group)"
done
for f in $(find "$CONFIG_DIR/services" -name "*.env" -type f 2>/dev/null | sort); do
    echo "  3. $f (service)"
done
