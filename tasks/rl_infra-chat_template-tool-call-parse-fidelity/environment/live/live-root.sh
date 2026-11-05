#!/bin/bash
# Root side of /opt/live/run.sh, run by the box's live service (/opt/live/liveserver.py): serve | run | status.
#   serve   start the engine (SGLang, Qwen3.5-2B, the H100) and the /generate endpoint on 127.0.0.1:30000
#   run     one live batch: SQL-agent and data-agent rollouts through /app/agent_rl (loop + launcher), see
#           /opt/live/py/live_job.py; record + batch log under /var/lib/agentrl-live, report in /tmp/live/run-<n>/
#   status  engine / endpoint state and the batches so far
set -u
[ "$(id -u)" = 0 ] || { echo "use /opt/live/run.sh" >&2; exit 2; }
umask 077
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin LANG=C.UTF-8
L=/opt/live; K=$L/state; S=/var/lib/agentrl-live; LOGD=/var/log/agentrl-live; OUTROOT=/tmp/live
ENGINE_PORT=31000; DEV_PORT=30000; ENGINE_WAIT=1200; JOB_TIMEOUT=2700; LOCK_WAIT=3300
CMD="${1:-}"
case "$CMD" in serve|run|status) ;; *) echo "usage: live-root.sh serve|run|status" >&2; exit 2 ;; esac
mkdir -p $K $S/runs $LOGD; chmod 0700 $K $S $S/runs $LOGD

say() { echo "[live $(date -u +%T)] $*"; }
event() { printf '{"utc":"%s","event":"%s"}\n' "$(date -u +%FT%TZ)" "$1" >> $S/events.jsonl; }
redact() { if [ -s $K/key ]; then sed -e "s/$(cat $K/key)/<key>/g"; else cat; fi; }
engine_up() { curl -sf -m 5 http://127.0.0.1:$ENGINE_PORT/health > /dev/null 2>&1; }
dev_up() { curl -sf -m 5 http://127.0.0.1:$DEV_PORT/health > /dev/null 2>&1; }
alive() { [ -s "$1" ] && kill -0 "$(cat "$1")" 2>/dev/null; }

start_engine() {
  [ -s $K/key ] || { head -c 24 /dev/urandom | od -An -tx1 | tr -d ' \n' > $K/key.tmp && mv $K/key.tmp $K/key; }
  engine_up && return 0
  if ! alive $K/engine.pid; then
    say "starting the engine (Qwen3.5-2B on the GPU; the first start takes a few minutes)"
    event engine_start
    setsid bash -c "cd /; echo \$\$ > $K/engine.pid; exec env -i \
      PATH=$L/venv/bin:/usr/local/cuda-12.8/bin:/usr/local/bin:/usr/bin:/bin CUDA_HOME=/usr/local/cuda-12.8 \
      HOME=/root LANG=C.UTF-8 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TIKTOKEN_ENCODINGS_BASE=/opt/tiktoken \
      TORCHINDUCTOR_COMPILE_THREADS=1 TRITON_CACHE_DIR=$K/triton \
      $L/venv/bin/python -I $L/engine.py >> $LOGD/engine.log 2>&1 < /dev/null" > /dev/null 2>&1 < /dev/null 9>&- &
    sleep 2
  fi
  local t=0
  while ! engine_up; do
    alive $K/engine.pid || break
    sleep 5; t=$((t + 5)); [ $t -ge $ENGINE_WAIT ] && break
    [ $((t % 60)) = 0 ] && say "  engine still starting (${t}s)"
  done
  if engine_up; then say "engine ready"; event engine_ready; return 0; fi
  say "the engine did not come up; last lines of its log:"; tail -25 $LOGD/engine.log | redact
  event engine_failed; return 1
}

start_dev_gateway() {
  dev_up && return 0
  alive $K/devgw.pid && kill "$(cat $K/devgw.pid)" 2>/dev/null
  setsid bash -c "cd /; echo \$\$ > $K/devgw.pid; exec python3 -I $L/gateway.py --listen-port $DEV_PORT \
     --engine-port $ENGINE_PORT --auth-file $K/key >> $LOGD/devgw.log 2>&1 < /dev/null" > /dev/null 2>&1 < /dev/null 9>&- &
  for _ in $(seq 1 30); do dev_up && return 0; sleep 1; done
  say "the /generate endpoint did not come up"; tail -5 $LOGD/devgw.log | redact; return 1
}

serve() {
  start_engine || return 1
  start_dev_gateway || return 1
  say "serving: POST http://127.0.0.1:$DEV_PORT/generate (input_ids, sampling_params, return_logprob), GET /health"
}

status() {
  engine_up && say "engine: up" || say "engine: down"
  dev_up && say "/generate on 127.0.0.1:$DEV_PORT: up" || say "/generate on 127.0.0.1:$DEV_PORT: down"
  for r in $(ls $S/runs 2>/dev/null | sort -n); do
    python3 -I -c 'import json, sys
r = json.load(open(sys.argv[1]))
print("run %s: %s, started %s, loop tree %s" % (r["run"], r["status"], r["started"], r["tree_sha256"][:16]))' \
      $S/runs/$r/record.json 2>/dev/null
  done
}

write_record() {  # run status tree files started [extra json]
  python3 -I - "$@" > $S/runs/$1/record.json.tmp <<'PY'
import json, sys
run, status, tree, files, started = sys.argv[1:6]
extra = json.loads(sys.argv[6]) if len(sys.argv) > 6 else {}
print(json.dumps({"run": int(run), "status": status, "tree_sha256": tree, "tree_files": int(files), "started": started,
                  "model": "qwen3.5-2b", **extra}, indent=1))
PY
  mv $S/runs/$1/record.json.tmp $S/runs/$1/record.json
}

prepare_workspaces() {
  rm -rf /work/ws; install -d -m 0755 /work/ws
  python3 -I - <<'PY'
import json, os, shutil
for line in open("/opt/live/data/data.jsonl"):
    if not line.strip():
        continue
    lab = json.loads(json.loads(line)["label"])
    ws, db = lab["workspace"], lab["db_id"]
    os.makedirs(ws)
    shutil.copy(f"/data/spider/databases/{db}/{db}.sqlite", os.path.join(ws, f"{db}.sqlite"))
    os.chmod(ws, 0o777)
    os.chmod(os.path.join(ws, f"{db}.sqlite"), 0o666)
PY
  chown -R liverun:liverun /work/ws
}

batch() {
  exec 9> $K/lock
  if ! flock -n 9; then
    say "waiting for another live batch or the engine start to finish"
    flock -w $LOCK_WAIT 9 || { say "gave up waiting"; return 1; }
  fi
  serve || return 1
  local N=$(( $(cat $S/counter 2>/dev/null || echo 0) + 1 )); echo $N > $S/counter
  local R=$S/runs/$N; mkdir -p $R; chmod 0700 $R
  local started; started=$(date -u +%FT%TZ)
  local th; th=$(python3 -I $L/treehash.py /app/agent_rl) || { say "cannot read /app/agent_rl"; return 1; }
  local tree=${th% *} files=${th#* }
  write_record $N started $tree $files $started
  say "run $N: loop tree /app/agent_rl sha256 $tree ($files code files)"
  prepare_workspaces
  setsid bash -c "cd /; echo \$\$ > $R/gw.pid; exec python3 -I $L/gateway.py --listen-port 0 --port-file $R/port \
     --engine-port $ENGINE_PORT --auth-file $K/key --log $R/traffic.jsonl >> $LOGD/batchgw.log 2>&1 < /dev/null" \
     > /dev/null 2>&1 < /dev/null 9>&- &
  for _ in $(seq 1 30); do [ -s $R/port ] && break; sleep 1; done
  if [ ! -s $R/port ]; then
    say "the batch gateway did not start"; write_record $N gateway_failed $tree $files $started; return 1
  fi
  local O=$OUTROOT/run-$N; install -d -m 0755 $OUTROOT; rm -rf $O; install -d -o liverun -g liverun -m 0755 $O
  say "run $N: rollouts start (per-rollout report in $O)"
  (cd /app/agent_rl && umask 000 && exec 9>&- && runuser -u liverun -- env -i PATH=/usr/local/bin:/usr/bin:/bin HOME=$O \
     LANG=C.UTF-8 PYTHONPATH=/app/agent_rl:/opt/miles:/opt/sglang/python:$L/py PYTHONDONTWRITEBYTECODE=1 \
     HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TIKTOKEN_ENCODINGS_BASE=/opt/tiktoken OMP_NUM_THREADS=2 \
     RAY_DISABLE_IMPORT_WARNING=1 SQL_AGENT_DB_ROOT=/data/spider/databases DATA_AGENT_WS_ROOT=/work/ws \
     DATA_AGENT_SANDBOX_CMD=/opt/live/sbx-client \
     timeout -k 30 $JOB_TIMEOUT python3 -s -B $L/py/live_job.py --port "$(cat $R/port)" --out $O < /dev/null 2>&1) \
     | (umask 022; tee $O/job.log) | grep --line-buffered -E '^\[live\]|Traceback|Error' | cut -c1-400
  local rc=${PIPESTATUS[0]}
  kill "$(cat $R/gw.pid)" 2>/dev/null; for _ in $(seq 1 20); do alive $R/gw.pid || break; sleep 1; done
  pkill -KILL -u liverun > /dev/null 2>&1; pkill -KILL -u nobody > /dev/null 2>&1
  local st=completed
  engine_up || st=engine_error
  [ "$st" = completed ] && [ "$rc" != 0 ] && st=job_failed
  gzip -f $R/traffic.jsonl 2>/dev/null
  local tsha=""; [ -s $R/traffic.jsonl.gz ] && tsha=$(sha256sum $R/traffic.jsonl.gz | cut -d' ' -f1)
  local stats; stats=$(python3 -I - $R/traffic.jsonl.gz <<'PY'
import collections, gzip, json, sys
c = collections.Counter()
try:
    for line in gzip.open(sys.argv[1], "rt"):
        c[str(json.loads(line).get("status"))] += 1
except Exception:
    pass
print(json.dumps(dict(c)))
PY
)
  local th2; th2=$(python3 -I $L/treehash.py /app/agent_rl); th2=${th2% *}
  write_record $N $st $tree $files $started "{\"ended\": \"$(date -u +%FT%TZ)\", \"job_exit\": $rc, \"traffic_sha256\": \"$tsha\", \"requests_by_status\": $stats, \"tree_sha256_after\": \"$th2\"}"
  # keep the batch logs of the last two completed runs (and of this one); records stay
  local keep; keep=$(for r in $(ls $S/runs | sort -n); do
    grep -q '"status": "completed"' $S/runs/$r/record.json 2>/dev/null && echo $r; done | tail -2)
  for r in $(ls $S/runs | sort -n); do
    [ "$r" = "$N" ] && continue; echo "$keep" | grep -qx "$r" && continue; rm -f $S/runs/$r/traffic.jsonl.gz
  done
  say "run $N: $st (job exit $rc; engine requests by HTTP status $stats)"
  [ "$th2" = "$tree" ] || say "run $N: WARNING: the loop tree changed while the batch ran"
  [ -s $O/summary.json ] && say "run $N summary: $(tr -d '\n ' < $O/summary.json)"
  [ "$st" = completed ]
}

case "$CMD" in
  serve)
    if engine_up && dev_up; then serve; exit $?; fi
    exec 9> $K/lock; flock -w $ENGINE_WAIT 9 || { say "a live batch is in progress"; exit 1; }
    serve ;;
  status) status ;;
  run) batch ;;
esac
