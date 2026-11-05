---
name: score-centering-sql-agent
description: Score centering (arXiv 2609.20807) added to /app/miles for the SQL-agent recipes; acceptance criteria and design decisions
metadata:
  node_type: memory
  type: project
  originSessionId: 8e4b5fcf-eaa9-4a75-b810-53a9ba3011aa
  modified: 2026-10-25T00:20:27.322Z
---

Score-centering loss (`--loss-type score_centering`, `--rollout-top-logprobs-num`, `--score-centering-is
none|tis|mis`) was implemented in /app/miles in Oct 2026 for the recipes `/app/launch/sql_agent_{session,native}.sh`.

**Why:** fp8 SGLang sampler vs bf16 Megatron trainer (cluster TP2 x CP2) mismatch; recipes also run at T=0.7.

**How to apply:** acceptance before merge = replay recorded rollouts at TP1/TP2/CP2 (8192 tokens/GPU, chunk 2048),
a live step of each recipe, TP2 x CP2 on recorded rollouts, and peak trainer memory on one 8192-token micro-batch at
TP1 at most 6 GiB above the PPO policy loss (measured: score centering is below PPO on both recipes). Key decisions:
candidates are recorded at generation time on `Sample.rollout_top_logprobs` (never rescored); under top-p/top-k
(sampling-support replay, recipe R1) they are restricted to the realized support and renormalized, and the trainer
normalizes p over the same support; with another `--loss-type` the score-centering flags only warn, so the PPO
baseline is the recipe plus `--loss-type policy_loss`.

Related: [[dev-box-runs]]
