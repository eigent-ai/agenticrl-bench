---
name: zero-pass-rl-insights
description: What worked / failed when RL-training Qwen3.5-4B (Miles plug-in) on tasks with zero base pass rate
metadata:
  node_type: memory
  type: project
  originSessionId: f564d39a-45a6-4a72-8d7e-c3bee5eba5ea
  modified: 2026-11-09T10:07:08.255Z
---

Zero-pass hill-climb task (Nov 2026, /opt/task, plug-in in /app/algo): learned signal came from
feedback-conditioned retries (checker report as an extra user message) whose tokens are trained under the plain
prompt (note tokens cut out), plus replay of stored passes and "success-conditioned" retries (note lists a passing
attempt's commands). Plain passes appeared ~8-10 steps after the first conditioned pass.

**Why:** all-zero GRPO groups give no gradient; partial credit rarely varies (same test fails every time).

**How to apply:**
- Shrink zero-advantage samples to 1 token (identical gradient, trainer time 590 s -> 70 s per step).
- Watch format errors per episode from the first hour: reinforcing passing episodes that contain format-error turns,
  and negative advantages on the action frame tokens (fence/tag/end-of-turn), eroded the harness tag
  (```bash, ```mswea, THOUGHT then stop). Fix: mask format-error / looping turns out of positives, keep the frame
  out of negatives, KL to base, lr <= 2.5e-6.
- Command lists / self-review hypotheses in failure notes did not help discovery; plain report notes did best.
- Loss-masking read-only turns of positives concentrated gradient on long heredocs -> repetition loops.
