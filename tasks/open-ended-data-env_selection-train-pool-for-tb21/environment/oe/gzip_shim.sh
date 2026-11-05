#!/bin/sh
# gzip-compatible shim, installed as /usr/local/bin/gzip (ahead of /usr/bin/gzip on PATH; the image build checks it).
# Harbor packs every directory artifact (and the agent logs) with `tar czf <file>` inside the box under a fixed 600 s
# timeout, and GNU tar runs `gzip` from PATH (through `sh -c gzip`). This shim:
#   1. compresses with pigz on all cores instead of single-threaded gzip (the output is standard gzip);
#   2. logs every pack into a file (Harbor's transfer archives; never the --stream trajectory sync, which runs
#      `tar -czf -` into a pipe every 2 s): start, pack seconds, bytes, rc and the tar command line, to
#      $OE_PRESUBMIT_STATE/shim.log.
# It no longer triggers the optional pre-download HF upload: the task's [[verifier.collect]] hook runs
# /usr/local/sbin/oe-presubmit-upload after the agent phase, before Harbor downloads the artifacts, with its own timeout.
# Decompression, test and list go straight to pigz (or gzip).
mode=c
for a in "$@"; do
  case "$a" in
    --stdout|--to-stdout|-c) ;;
    --decompress|--uncompress|--test|--list) mode=d ;;
    --*) ;;
    -*[dtl]*) mode=d ;;
  esac
done
Z=""
command -v pigz >/dev/null 2>&1 && Z=pigz
if [ -z "$Z" ]; then
  for g in /usr/bin/gzip /bin/gzip; do
    [ -x "$g" ] && { Z="$g"; break; }
  done
fi
[ -n "$Z" ] || { echo "gzip shim: no pigz or gzip found" >&2; exit 127; }
if [ "$mode" != c ] || [ ! -f /dev/stdout ]; then
  exec "$Z" "$@"
fi
S="${OE_PRESUBMIT_STATE:-/var/lib/oe-presubmit}"
# the tar that runs us (through `sh -c gzip`), for the log
pk=$PPID
for _ in 1 2 3; do
  case "$(cat /proc/$pk/comm 2>/dev/null)" in tar) break ;; esac
  pk=$(awk '{print $4}' /proc/$pk/stat 2>/dev/null || echo 1)
done
t0=$(date +%s.%N)
t1=$t0
"$Z" "$@"
rc=$?
out=$(readlink /proc/$$/fd/1 2>/dev/null)
sz=$(stat -c %s "$out" 2>/dev/null || echo -1)
t2=$(date +%s.%N)
mkdir -p "$S" 2>/dev/null && awk -v a="$t0" -v b="$t1" -v c="$t2" -v z="$sz" -v r="$rc" -v o="$out" -v u="$(date -u +%FT%TZ)" \
  -v d="$(tr '\0' ' ' < /proc/$pk/cmdline 2>/dev/null | cut -c1-200)" \
  'BEGIN { printf "%s start=%.3f pack_s=%.1f bytes=%s rc=%s out=%s tar=%s\n", u, a, c - b, z, r, o, d }' \
  >> "$S/shim.log" 2>/dev/null
exit $rc
