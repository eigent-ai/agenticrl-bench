---
name: sql-rescue-findings
description: "Outcome of the Oct 2026 rescue-of-all-failed-groups investigation (stale prefix cache, rescue vs plain GRPO)"
metadata:
  node_type: memory
  type: project
  originSessionId: 693819a0-56c7-47e9-b47d-c10f431747ae
  modified: 2026-10-25T00:53:08.725Z
---

2026-10-24: with in-place weight pushes, stock Miles never flushes SGLang's prefix cache; for hybrid Qwen3.5 (GDN,
`extra_buffer`) the shared system prefix's state stays from the first weights, so every rollout/eval is conditioned on
stale state. That caused the train/rollout KL creep (plain GRPO too) and inflated in-run evals. Fix lives in
`examples/sql_agent/rescue/rollout.py` (flush on weight-version change when idle); details and numbers in `/app/NOTES.md`.

Even fixed (MH acceptance, scratch scoring), the rescue lost ~0.3 pass@1 to plain GRPO over 50 steps; the user was told
not to ship it as is. Single-run evals of the hard set swing ±0.04 — use the clean-cache harness (`/root/tools/eval_ckpts.py`).

**Why:** future sessions on this project will likely revisit the rescue or the production job's cache behaviour.
**How to apply:** start from `/app/NOTES.md`; verify current code before relying on this. Related: [[sql-rl-constraints]].
