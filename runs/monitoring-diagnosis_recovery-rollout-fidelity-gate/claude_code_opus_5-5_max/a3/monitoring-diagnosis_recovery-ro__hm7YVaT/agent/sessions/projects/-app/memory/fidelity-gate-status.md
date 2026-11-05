---
name: fidelity-gate-status
description: State of the /app/fidelity rollout-fidelity gate as of 2026-10-25 and the one open judgment call (kv-fp8-e4m3)
metadata:
  node_type: memory
  type: project
  originSessionId: 1d8adf64-d665-4ff7-8ceb-55e2f305e7f3
  modified: 2026-10-25T07:27:09.291Z
---

Built 2026-10-25: `/app/fidelity/check` (+ fidelity_check.py, NOTES.md). All 11 queued changes screened; verdicts and
evidence are in NOTES.md. HOLD: prefill-only deterministic, deterministic, top-p 0.98, int8 mamba ckpt, kv-fp8-e5m2.
SAFE: MTP, page-64, mixed-chunk, ssm-fp16, triton-attn, kv-fp8-e4m3 (plus prod/quiet-logging/TP2).

**Why:** the user asked for a gate on "does the engine still give GRPO the samples it assumes"; the mismatch panel
failed both ways.

**How to apply:** kv-fp8-e4m3 is the deliberate borderline (typical engine/trainer KL ~2.8–3.0× production; the line
is 4×, `KL_FACTOR`). If the user reports e4m3 hurting long runs, lowering to 2.5 is the documented alternative.
Reference constants (C/D) are tied to the Qwen3.5-2B base checkpoint and only use rollout steps 0–2.
Related: [[miles-runs-outside-screen-service]].
