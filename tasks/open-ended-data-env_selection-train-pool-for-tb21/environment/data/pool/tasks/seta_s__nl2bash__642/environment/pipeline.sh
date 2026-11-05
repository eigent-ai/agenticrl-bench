#!/bin/bash
set -e
BASEDIR="/opt/medialib"
SCRIPTS="$BASEDIR/scripts"

echo "=== Image Cataloging Pipeline ==="
echo "Phase 1: Discovery..."
"$SCRIPTS/discover.sh"

echo "Phase 2: Validation..."
"$SCRIPTS/validate.sh"

echo "Phase 3: Manifest Build..."
"$SCRIPTS/build_manifest.sh"

echo "=== Pipeline Complete ==="
