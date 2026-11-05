#!/bin/bash
set -euo pipefail

cd /opt/metrics

find jcho -name '*.data' -not -name '.*' -type f | while read -r f; do
    # Strip the leading "jcho/" prefix, then replace all "/" with "_"
    flat=$(echo "$f" | sed 's~^jcho/~~' | tr '/' '_')
    cp "$f" "export/$flat"
done
