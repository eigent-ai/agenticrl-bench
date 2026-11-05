#!/bin/bash
n=$(curl -s numbers.internal/next/ticket | python3 -c 'import json,sys;print(json.load(sys.stdin)["value"])')
mkdir -p tickets
printf '# %s\n\nstatus: new\n' "$1" > "tickets/T-$n.md"
echo "created ticket"
