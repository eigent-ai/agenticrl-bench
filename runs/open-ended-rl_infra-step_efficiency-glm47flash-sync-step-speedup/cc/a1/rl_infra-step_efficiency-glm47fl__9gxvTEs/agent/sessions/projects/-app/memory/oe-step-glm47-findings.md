---
name: oe-step-glm47-findings
description: "Measured bottlenecks and what worked/failed when speeding up the GLM-4.7-Flash synchronous GRPO step (Miles+SGLang, 4xH200, OE-STEP bench)"
metadata:
  node_type: memory
  type: project
  originSessionId: b83c6cf9-26a6-4ec8-ab0c-bbbb1515591e
  modified: 2026-10-26T10:17:42.098Z
---

Session 2026-10-26 (task: make the synchronous agentic-RL step faster; bench at /opt/oe-step, launch in /app/launch).
Result: 645 s -> 484 s per step (1.33x), all gates pass; details in /app/NOTES.md.

- Rollout makespan = engine 2's 16 episodes (one 37k-token episode); single-engine subset replay reproduces it, so
  4 engine configs can be A/B'd in parallel on 4 GPUs with a standalone replay harness.
- SGLang served logprobs are nondeterministic at mean |d| ~0.047 between identical engines (EAGLE verify chunking):
  the served-logprob gate's noise floor; strict bench cap 0.0647.
- Wins: skip ref model (kl coef 0), --skip-actor-forward-only + capture train log-probs for the dump, breakable
  prefill CUDA graphs (needs SGLANG_MEMORY_SAVER_CUDA_GRAPH=false), tuned fused-MoE triton config, single-group
  router shortcut, selective + per-micro-batch recompute, pinned CPU-Adam masters, trainer keeps non-param memory
  resident while asleep (with max_split_size_mb:512 and a 20 GiB guard).
- No-recompute micro-batches leave small long-lived blocks (RoPE lru_cache, router routing maps, TE dummy wgrads)
  pinning large allocator segments -> memory-saver pause cost or OOM if kept resident.
- Failed: TP4/TP2/DP-attention engine layouts, more draft tokens, FlashMLA, batch caps.
