---
name: tb21-rl-session-plan
description: "Key constraints discovered for the TB2.1 GRPO task (Qwen3.5-4B, /opt/task/scripts) and the chosen plan"
metadata:
  node_type: memory
  type: project
  originSessionId: 4b0e96c1-1d51-4871-b378-cca3fedc956c
  modified: 2026-11-09T04:03:32.412Z
---

Session started 2026-11-09 ~03:58 UTC, 16 h budget (ends ~19:55 UTC).

Facts learned from the scripts (verify they still hold if reused):
- train.py has no --from: every training run starts from the base model, so stopping a run to eval loses it. One GPU job at a time (train OR eval).
- Trainer filter fixed at no_aborted: all-pass / all-fail GRPO groups give zero gradient, so pick tasks with intermediate pass rates.
- Training episodes: 200 calls, 600 s wall cap (capped episodes are dropped from the gradient), max_seq_len <= 49152. Eval: 1000 calls, 128k ctx.
- Rewards are binary (test.sh writes 1/0) for both TMax and SETA pool tasks.
- Base TB2.1 failures: ~90% are "submitted but wrong" (partial tests pass); there are few context/format failures.

Plan: screen ~540 pool tasks with eval.py (k=4), select intermediate-pass-rate tasks, run one long GRPO run, eval checkpoints at the end, export the best.

Pool gotcha found mid-run: SETA verifiers (tests/test.sh) download uv / CPython / pytest from GitHub/PyPI at test time;
GitHub release downloads started returning 504 (~13% of SETA training episodes scored 0 regardless of work). Fix used:
keep the original as tests/test_orig.sh and make test.sh a retry wrapper that re-runs it while no pytest session ran
(/app/work/repair/). Train-time Triton autotune (fla causal_conv1d, key NB=cdiv(B*T,1024)) makes the first steps slow;
steady state is ~12-13 min/step (rollout ~610 s is bound by the 600 s wall cap).

Outcome (2026-11-09): exported grpo1 iter_27 (28 steps). Lessons:
- GRPO on short pool tasks first made the model hasty on TB2.1 (iter_15: ~35% fewer steps, worse). It recovered
  after ~25 steps, and lr 3e-6 caused fence-tag drift (`bswea_bash_command`) after ~15 steps there.
- Compare checkpoints against each other under same-day conditions, not against the October diagnostics: same-day
  scores were much lower (near-base subset score 0.42 against 0.56 in the diagnostics). A cheap, sharp comparison is
  the 30 TB2.1 tasks the base ever solves, with k=8.
- Stopping a run mid-save leaves an unusable last checkpoint (no config.json); stop right after a save completes.
