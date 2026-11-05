---
name: sandbox-broker-facts
description: "Measured behaviour of the sandbox broker / Modal gVisor sandboxes used for terminal-RL tasks on this box (capabilities, entrypoint, PATH/PYTHONPATH, tmux harness traps)"
metadata:
  node_type: memory
  type: reference
  originSessionId: f00f231a-f107-44ff-b715-22f86aecc2e0
  modified: 2026-10-24T23:28:23.023Z
---

Measured 2026-10-24 on the training-style sandboxes (`sandbox` CLI, `sandbox_broker.harbor_env:BrokerEnvironment`):

- Broker only starts `environment/` dirs whose content hash is in `/etc/sandbox-broker/build-contexts.txt`;
  any edit under `environment/` makes a task unrunnable here (validate image changes with a copy that keeps
  the original env and applies the change via `[environment.healthcheck]`). Audit log with every exec's argv:
  `/var/log/sandbox-broker/audit.jsonl` (readable; great for tracing what killed an episode).
- gVisor; root's bounding set lacks SYS_ADMIN, NET_ADMIN, NET_RAW, SYS_TIME, SYS_NICE, LINUX_IMMUTABLE...
  (no mount, no packet capture, file caps with +ep on those make binaries unexecutable for non-root).
- PID 1 = `dumb-init -- <ENTRYPOINT> sh -c 'sleep infinity'`: ENTRYPOINT runs, CMD is replaced. Killing that
  sleep / `kill -HUP 1` ends the sandbox (BackendFailure).
- Sandbox env sets `PYTHONPATH=/pkg/:/root/`. `uvx ... pytest` puts its env's bin/ (python3!) first on PATH
  for tests; the hardened runner runs `$RUNNER_PY -P -s -m pytest` instead.
- Harbor verifier reads `/logs/verifier/reward.json` before reward.txt; agent is root, so test.sh must delete
  stale reward files and ignore conftest/pytest.ini (`-c /dev/null --noconftest`).
- Terminus-2's terminal is the only pane of tmux session `terminus-2` on the default socket: `exit`,
  `tmux kill-server`, `pkill bash`, `exec cmd` in it => RuntimeError "no server running", no reward.

Related: [[terminal-rl-pool-audit-2026-10]]
