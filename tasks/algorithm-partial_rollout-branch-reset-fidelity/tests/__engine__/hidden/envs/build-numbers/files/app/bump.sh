#!/bin/bash
if [ "$1" = "--dry-run" ]; then echo "would bump $(cat VERSION)"; exit 0; fi
n=$(curl -s seq.internal/next/build | python3 -c 'import json,sys;print(json.load(sys.stdin)["value"])')
echo "$(cut -d. -f1-2 VERSION).$n" > VERSION
echo bumped
