---
name: miles-runs-outside-screen-service
description: "How to launch extra Miles/SGLang recipe runs on the /app box without breaking the screening service (Ray ports, HOME, DeepGEMM cache, time limits)"
metadata:
  node_type: memory
  type: reference
  originSessionId: 1d8adf64-d665-4ff7-8ceb-55e2f305e7f3
  modified: 2026-10-25T07:27:04.847Z
---

Running the SQL-agent recipe outside `/app/queue/run_screen.sh` (e.g. production-recipe short runs with lr>0):

- Launch with `HOME=<own dir> PYTHONPATH=/root/Megatron-LM/:/root/miles python3 -s /app/queue/run_screen.py <command.txt>`;
  `--save-debug-train-data` must point to a dir you own (`/app/runs` is root's).
- Miles' launcher runs `pkill`/`ray stop` and takes Ray's default ports: never overlap a service screen
  (`run_screen.sh --status` active must be None), and `ray stop --force` afterwards.
- Deterministic-inference flags make SGLang JIT DeepGEMM into `/tmp/sglang_deep_gemm/...`, owned by the service user
  (`rlscreen`) after any service screen → errno 13. Fix: add `SGLANG_DG_CACHE_DIR=<own dir>` to the command's
  `# env:` header line (run_screen.py passes it to the job env; Miles' server_group reads it).
- Background shell tasks die at 2 h: use runners that skip already-completed screens (re-requesting a completed
  change could re-screen it).
- `pkill -f <pattern>` also matches the invoking shell if the pattern is in its command line.

See [[fidelity-gate-status]].
