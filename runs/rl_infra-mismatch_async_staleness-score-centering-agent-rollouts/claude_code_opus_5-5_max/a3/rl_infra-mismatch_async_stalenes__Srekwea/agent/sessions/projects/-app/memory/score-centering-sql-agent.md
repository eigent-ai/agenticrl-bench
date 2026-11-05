---
name: score-centering-sql-agent
description: Score centering (arXiv 2609.20807) added to /app/miles for the SQL-agent recipes; design choices and how it was verified (2026-10-25)
metadata:
  node_type: memory
  type: project
  originSessionId: a2a72cd3-7920-4095-aca4-96407d24d055
  modified: 2026-10-25T05:02:04.385Z
---

Score centering (`--loss-type score_centering`, `--rollout-top-logprobs-num`, `--score-centering-is none|tis|mis`) was implemented in /app/miles on 2026-10-25 for the two recipes in /app/launch (session v2 = TIS, native multi-turn = MIS). Pristine pre-change snapshot was copied to /tmp/orig/miles (may not survive).

Design decisions the user should not have to rediscover:
- top_p<1 or top_k>0 auto-enables sampling-support replay; then the sampler head is SGLang's support-normalized log-probs (`sampling_logprobs_mode="support"`), not the untruncated top-k — the behavior distribution is the truncated one.
- SC flags only warn (not error) under other loss types so a launcher can A/B by swapping `--loss-type` alone (e.g. the PPO memory comparison).
- SC requires `--use-rollout-logprobs`; refuses --recompute-logprobs-via-prefill, --use-tis, --use-opsm, gspo, --allgather-cp, true-on-policy, non-megatron backends, OPD student top-k.

**Why:** the user's merge gate replays recorded rollouts at TP1/TP2/CP2, runs live steps of both recipes, checks TP2xCP2 on recordings, and caps SC peak memory at PPO + 6 GiB on an 8192-token TP1 micro-batch.
**How to apply:** measured real-trainer peaks: native SC +0.48 GiB vs PPO, session SC -4.4 GiB; loss-only bench -3.4/-4.3 GiB. Peak-memory hook approach: `--custom-megatron-before-train-step-hook-path` wrapping optimizer.step. See [[offline-dev-box-testing]].
