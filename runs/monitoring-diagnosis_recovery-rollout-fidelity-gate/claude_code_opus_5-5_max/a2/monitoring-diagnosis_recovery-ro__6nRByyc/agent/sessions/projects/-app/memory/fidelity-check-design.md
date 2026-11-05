---
name: fidelity-check-design
description: "Non-obvious findings behind /app/fidelity/check (why mismatch metrics fail, which signals work) for the SQL-agent GRPO recipe"
metadata:
  node_type: memory
  type: project
  originSessionId: 5dc14ac7-e828-428f-b84f-26ad34dc4d00
  modified: 2026-10-25T00:42:23.588Z
---

Built 2026-10-24/25. The check gates rollout-engine changes on "does the engine give GRPO the samples it assumes".

- Mismatch panel (mean |dlogp|) is useless as a gate: ~5% of samples drift late in long answers and dominate it.
- Working signals: within-group prefix-tree collision test (copies), slot-identity + repeated near-impossible
  tokens (frozen per-slot seeds), Hill tail depth + rate (truncation, e.g. top-p), 25th-pct of
  |dlogp|/sum(1-p) (engine numerics, hold > sqrt(2) x prod).
- Queue verdicts: HOLD prefill-deterministic, deterministic, top-p-098, kv-fp8-e4m3/e5m2, int8-mamba-ckpt;
  SAFE mtp-nextn, ssm-fp16, triton-attn, page-64, mixed-chunk (details in /app/fidelity/NOTES.md).
- Calibration constants assume the Qwen3.5-2B base policy; recalibrate if the checkpoint changes.

**Why:** the team lost a week to a change the panel passed. **How to apply:** extend the check rather than
re-deriving; see [[screening-box-workflow]] for running new screens.
