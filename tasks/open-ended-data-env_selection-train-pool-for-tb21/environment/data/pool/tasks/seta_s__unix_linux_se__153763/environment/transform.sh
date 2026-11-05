#!/bin/bash
# Transform processed data: compute row sums
input="$1"
output="$2"
if [ -z "$input" ] || [ -z "$output" ]; then
    echo "Usage: transform.sh <input> <output>" >&2
    exit 1
fi
while IFS=',' read -r line; do
    sum=0
    for val in $(echo "$line" | tr ',' ' '); do
        sum=$((sum + val))
    done
    echo "$line,sum=$sum"
done < "$input" > "$output"
