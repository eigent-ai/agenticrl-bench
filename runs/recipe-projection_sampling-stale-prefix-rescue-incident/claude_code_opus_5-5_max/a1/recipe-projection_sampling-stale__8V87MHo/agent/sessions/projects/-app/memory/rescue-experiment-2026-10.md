---
name: rescue-experiment-2026-10
description: "Findings from debugging the SQL-agent GRPO rescue (hinted projection sampler) on Miles+SGLang, Oct 2026"
metadata:
  node_type: memory
  type: project
  originSessionId: 899210cc-9d6a-4ccc-8ca6-13bd419d22ae
  modified: 2026-10-24T22:23:47.448Z
---

Rescue of all-failed GRPO groups (`/root/miles/examples/sql_agent/rescue/`, launcher `/app/launch/run_sql_rl.py`) was
debugged on 2026-10-24; the write-up is `/app/NOTES.md`, scripts/probes in `/app/scratch/`, runs in `/app/runs/`.

Key facts that are not obvious from the code:
- With `--pause-generation-mode in_place`, Miles never flushes SGLang's prefix cache; on the hybrid Qwen3.5 model the
  shared system+tool prompt state from step 0 was reused all run (stale state → creeping train/rollout KL).
- SGLang (stock, this box) corrupts some decode-tracked linear-attention states under concurrent decode; resuming a
  later turn from them shifts the distribution (probe: `/app/scratch/continuation_probe3.py`). Affects plain GRPO too.
- Plain GRPO alone takes held-out hard accuracy 7% → 41% in 50 steps; the original rescue made it far worse (11%).
  Full-weight injected hinted runs dominate the gradient and teach answering early; see [[rescue-eval-method]].
- Shipped fix (v6): only tokens with pi_proposer <= tis_clip * pi_student are trained, student behaviour log-probs,
  failed siblings `remove_sample`, cache flush per rollout/eval, fresh `extra_key` per rescue request, hint-talk
  regex in "passes". Result: hard 40.2% (= plain GRPO 40.6%), regular 75% vs 85%; agreement flat. No payoff yet.

**Why:** user wants the rescue shipped with the recipe unchanged (in-place pushes, stock Miles/SGLang, fixes only in
our tree). **How to apply:** compare rescue variants against plain GRPO with paired per-step pass rate and the
checkpoint eval, not the noisy in-run eval.
