---
name: agent-proxy-rewrite
description: "State of the terminal_rl agent proxy rewrite (2026-10-24): design, open decisions, how it was verified"
metadata:
  node_type: memory
  type: project
  originSessionId: 6704db28-84ee-4c36-bef8-76c1584552a3
  modified: 2026-10-24T21:12:32.916Z
---

On 2026-10-24 the proxy in /app/terminal_rl/terminal_rl/proxy was rewritten while the owner was away for the week:
- It mirrors SGLang 0.5.9's chat endpoint (render.py).
- It keeps a per-agent prefix trie so the engine's earlier ids are reused instead of re-tokenized (session.py).
- Identical bodies are treated as retries and deduplicated; engine aborts are re-run.
- Only delivered generations are trained, and rows are assembled at finish.

Verification lives in tools/audit_replay.py, tests/test_proxy.py and replay_traffic.py --drop-rate. Findings are in
/app/NOTES.md.

**Why:** the GLM-4.7-Flash switch exposed wrong prompts, merged explorer rows, and trained partial or undelivered
generations.

**How to apply:** decisions still open for the owner:
- Sampling defaults now follow generation_config, like SGLang: Qwen gets top_k=20, top_p=0.8. Use
  `--sampling-defaults openai` to revert.
- `--context-length` is informational only.
- An aborted generation is re-run from scratch, so a long generation can starve under frequent weight updates.

Check NOTES.md before changing any of these. See also [[live-run-tool]].
