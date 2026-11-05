---
name: sandbox-infra-facts
description: "Measured properties of the box's sandbox service (Modal/gVisor) that matter for timing-sensitive tests"
metadata:
  node_type: memory
  type: reference
  originSessionId: 34ede423-7288-47d4-a58f-8f33976822a5
  modified: 2026-10-24T19:53:26.465Z
---

Measured 2026-10-24 on the pool box (sandbox CLI / sandbox_broker client, Modal + gVisor):
- Only the 33 registered build contexts start; changing a task's environment/ makes it unstartable here and
  "not_started" in run_grpo.sh runs. Test such a change by starting from a pristine copy of the context and
  uploading the changed file.
- Idle workers differ ~2.6x in CPU speed (3M-iteration Python loop: 0.05-0.13 s); absolute timing thresholds are
  node-dependent even without load.
- gVisor charges throttled/descheduled time as user CPU time, so process_time() is not load-robust.
- `--cpu 0.25` (quota) lets ~0.1 s bursts run unthrottled: short calibration loops underestimate slowdown.
- Emulating stalls with SIGSTOP/SIGCONT of all processes distorts allocation-heavy code (pygame surface copies)
  under gVisor far more than real stalls; use CPU hogs / quota for those.
- Image CMD/ENTRYPOINT does not run in sandboxes (PID 1 is dumb-init + sleep); Xvfb etc. are not pre-started.
- /proc/net/tcp and /proc/net/udp work inside sandboxes (usable for readiness checks).
Related: [[reward-fix-constraints]], [[pool-reward-fix-2026-10]].
