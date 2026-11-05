#!/bin/bash
# Compare actual NFS mounts against expected configuration

SERVER="$1"
ACTUAL_MOUNTS="$2"
EXPECTED_MOUNTS="$3"

# Create sorted lists for comparison
ACTUAL_SORTED=$(echo "$ACTUAL_MOUNTS" | grep -v '^$' | sort)
EXPECTED_SORTED=$(echo "$EXPECTED_MOUNTS" | grep -v '^$' | sort)

# Find missing mounts (expected but not actual)
MISSING=$(comm -23 <(echo "$EXPECTED_SORTED") <(echo "$ACTUAL_SORTED"))

# Find extra mounts (actual but not expected)
EXTRA=$(comm -13 <(echo "$EXPECTED_SORTED") <(echo "$ACTUAL_SORTED"))

# Output discrepancies
while IFS= read -r mount; do
    [ -z "$mount" ] && continue
    echo "${SERVER}|${mount}|MISSING"
done <<< "$MISSING"

while IFS= read -r mount; do
    [ -z "$mount" ] && continue
    echo "${SERVER}|${mount}|EXTRA"
done <<< "$EXTRA"
