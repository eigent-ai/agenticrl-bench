---
name: harbor-token-accounting-vs-qwen
description: "Harbor budgets context with cl100k via litellm, while SGLang tokenizes with Qwen — 1.25x on log output, 1.7x on byte dumps"
metadata:
  node_type: memory
  type: project
  originSessionId: 99458fb9-bd10-4788-b317-ad3bfb8be2f6
  modified: 2026-10-25T00:22:33.979Z
---

`litellm.token_counter(model="hosted_vllm/policy", …)` does not recognise the model and falls back to
cl100k_base (gpt-3.5-turbo), so every Harbor context decision — proactive summarization at 8000 free
tokens, `_unwind_messages_to_free_tokens` — is made in cl100k tokens while the server tokenizes with
Qwen3.5. Measured Qwen/cl100k: ~0.98 on prose, ~1.25 on terminal/log output, ~1.69 on byte dumps
(`od` output).

**Why:** on the TB2.1 eval path `model_info.max_input_tokens` (65536) equals the served context, so a
log-heavy trial can be rejected by the server before Harbor thinks it is near the limit — and
unwinding to "4000 free" in cl100k still leaves the real prompt over, so the trial never recovers and
burns its agent timeout making 400s. The RL rollouts budget 32768 against a 65536 server, so they have
the headroom to absorb the gap.

**How to apply:** when a long eval trial dies at its agent timeout with context-length 400s, this is
the first thing to check; lowering the eval's declared `max_input_tokens` (or raising the served
context) restores the margin. Related: [[harbor-truncated-xml-salvage-bug]].
