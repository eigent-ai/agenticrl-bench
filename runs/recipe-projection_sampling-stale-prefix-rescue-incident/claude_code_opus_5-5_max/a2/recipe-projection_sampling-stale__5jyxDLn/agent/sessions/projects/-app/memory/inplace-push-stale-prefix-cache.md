---
name: inplace-push-stale-prefix-cache
description: "Miles v0.1.0 in_place weight pushes never flush SGLang's radix cache; stale prefix KV/GDN state silently inflates train/rollout KL"
metadata:
  node_type: memory
  type: project
  originSessionId: 13ae4349-f5f2-41b3-85da-fe20c58217f5
  modified: 2026-10-24T22:30:44.658Z
---

On this box (Miles v0.1.0, SGLang 0.5.17.dev, Qwen3.5-2B hybrid GDN, mamba extra_buffer radix cache),
`--pause-generation-mode in_place` makes Miles skip `flush_cache` on every weight push. Prefix KV and
GDN states computed under old weights keep being reused. The shared 320-token system prompt was computed
at eval 0 and reused for the whole run, so `train/train_rollout_kl` crept 10x over 50 steps. The same
happens in plain GRPO, not only with the rescue.

Diagnosis trick: score the same tokens via prefill with a unique `extra_key`, then without one; the
difference is staleness. The router passes `extra_key` through. Within one weight version, prefix reuse is
exact. Reusing a state from a branching point gives ~0.005 nats/token of numerical noise even without
staleness.

**Why:** user ships in_place pushes (production async job) and won't patch Miles/SGLang.
**How to apply:** fixes go in our tree. The rescue code in `examples/sql_agent/rescue/engine_cache.py` flushes
at rollout start when the weight version has changed. Scoring uses private `extra_key`s.
Related: [[sql-rescue-hint-leakage]]
