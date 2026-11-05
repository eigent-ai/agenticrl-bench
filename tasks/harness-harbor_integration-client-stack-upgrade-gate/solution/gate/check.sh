#!/bin/bash
set -uo pipefail
G=$(cd "$(dirname "$0")" && pwd)
V=$(realpath "${1:?usage: check.sh <venv>}")
REF_PY=/opt/venvs/client/bin/python
[ -x "$V/bin/python" ] || { echo "not a venv: $V"; exit 2; }
W=$(mktemp -d "${TMPDIR:-/tmp}/gate.XXXXXX")
trap 'rm -rf "$W"' EXIT
echo "candidate: $("$V/bin/python" -c 'import importlib.metadata as m; print("harbor", m.version("harbor"), "litellm", m.version("litellm"))' 2>&1 | tail -1)"
if [ -n "${ENGINE_URLS:-}" ]; then
  : "${ENGINE_LOG_DIR:?live mode needs ENGINE_LOG_DIR}"
  EXCL=${GATE_LIVE_EXCLUDE-long_}
  "$REF_PY" -I "$G/live.py" snapshot "$ENGINE_LOG_DIR" "$W/snap.json"
  if ! GATE_RUN_ID=ref "$REF_PY" "$G/rig/run_battery.py" "$G/battery" "$W/ref" --procs "${GATE_PROCS:-4}" \
       --exclude "$EXCL" > "$W/ref.log" 2>&1; then
    echo "UNSAFE?: the reference replay through the servers failed"; tail -5 "$W/ref.log"; exit 1
  fi
  if ! GATE_RUN_ID=cand "$V/bin/python" "$G/rig/run_battery.py" "$G/battery" "$W/cand" --procs "${GATE_PROCS:-4}" \
       --exclude "$EXCL" > "$W/run.log" 2>&1; then
    echo "UNSAFE: the replay does not run on this stack"; tail -5 "$W/run.log"; exit 1
  fi
  "$REF_PY" -I "$G/confirm.py" "$V" "$G/battery" "$W/ref" "$W/cand" >> "$W/run.log" 2>&1 || true
  "$REF_PY" -I "$G/confirm.py" /opt/venvs/client "$G/battery" "$W/cand" "$W/ref" >> "$W/run.log" 2>&1 || true
  "$V/bin/python" -I "$G/tokprobe.py" "$G/ref/probe_msgs.jsonl" > "$W/tok.txt" 2>> "$W/run.log" || echo "token probe failed" >> "$W/run.log"
  "$REF_PY" -I "$G/live.py" collect "$ENGINE_LOG_DIR" "$W/snap.json" "$W/engine.json"
  [ -n "${GATE_REPORT:-}" ] && "$REF_PY" -I "$G/live.py" report "$W/engine.json" "$GATE_REPORT"
  "$REF_PY" -I "$G/compare.py" "$G/battery" "$W/ref" "$W/cand" "$G/ref/tok.txt" "$W/tok.txt" --engine "$W/engine.json"
  rc=$?
  KEEP=${GATE_KEEP:-$(cat "$G/.keep" 2>/dev/null || true)}
  [ -n "$KEEP" ] && mkdir -p "$KEEP" && cp -r "$W" "$KEEP/"
  exit $rc
fi
if ! "$V/bin/python" "$G/rig/run_battery.py" "$G/battery" "$W/cand" --procs "${GATE_PROCS:-4}" > "$W/run.log" 2>&1; then
  echo "UNSAFE: the replay does not run on this stack"; tail -5 "$W/run.log"; exit 1
fi
"$REF_PY" -I "$G/confirm.py" "$V" "$G/battery" "$G/ref/run" "$W/cand" >> "$W/run.log" 2>&1 || true
"$V/bin/python" -I "$G/tokprobe.py" "$G/ref/probe_msgs.jsonl" > "$W/tok.txt" 2>> "$W/run.log" || echo "token probe failed" >> "$W/run.log"
"$REF_PY" -I "$G/compare.py" "$G/battery" "$G/ref/run" "$W/cand" "$G/ref/tok.txt" "$W/tok.txt"
