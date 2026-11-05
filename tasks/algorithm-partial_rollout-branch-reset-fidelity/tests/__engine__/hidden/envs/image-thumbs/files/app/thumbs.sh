#!/bin/bash
# usage: thumbs.sh [--lock] <in dir> <out dir>
LOCK=0
if [ "$1" = "--lock" ]; then LOCK=1; shift; fi
IN=$1; OUT=$2
mkdir -p "$OUT"
[ $LOCK = 1 ] && echo $$ > "$OUT/.lock"
for f in "$IN"/*.img; do
  sleep 0.35
  b=$(basename "$f" .img)
  head -c 48 "$f" | od -An -tx1 | tr -d ' \n' > "$OUT/$b.thumb"
  echo "$b" >> "$OUT/manifest.txt"
done
echo "thumbs: $(wc -l < "$OUT/manifest.txt") done"
