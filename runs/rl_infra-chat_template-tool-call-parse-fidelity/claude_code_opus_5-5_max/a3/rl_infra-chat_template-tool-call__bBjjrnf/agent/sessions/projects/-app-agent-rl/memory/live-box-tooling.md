---
name: live-box-tooling
description: "Facts about the agent_rl box's live engine and batch runner that are not obvious from the code (determinism, sandbox access, tree hash)"
metadata:
  node_type: memory
  type: reference
  originSessionId: bb4284c4-f090-47c0-ad63-87b6aefd7156
  modified: 2026-11-11T13:12:25.153Z
---

- `/opt/live/run.sh run` runs one live batch (Qwen3.5-2B, 128 SQL + 32 data rollouts, ~1 min) and records the sha256
  of the code tree in /app/agent_rl at start and end; the user keeps the batch run with the final loop, so run it only
  after the last code change (NOTES.md in /app is outside the tree). Report: /tmp/live/run-N/samples.jsonl.
- The dev endpoint 127.0.0.1:30000/generate passes sampling params through; the engine is NOT deterministic even with
  `sampling_seed`, so old-vs-new loop comparisons need tools/replay.py-style replays of recorded traffic.
- The data agent's sandbox socket (/run/agentrl-live/sbx) is only usable by the live service's user; own dev runs can
  use real execute_sql but should stub the shell.
- An argparse "error: the following arguments are required: --rollout-batch-size" dump in replay/live logs is harmless.

Related: [[agent-rl-tool-call-reader]]
