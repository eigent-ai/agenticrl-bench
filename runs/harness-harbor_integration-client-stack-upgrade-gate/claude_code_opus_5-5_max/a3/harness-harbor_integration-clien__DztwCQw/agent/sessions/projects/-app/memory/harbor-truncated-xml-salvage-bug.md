---
name: harbor-truncated-xml-salvage-bug
description: Harbor 0.23/0.24 Terminus-2 kills a trial with AttributeError when it salvages a truncated XML response
metadata:
  node_type: memory
  type: project
  originSessionId: 99458fb9-bd10-4788-b317-ad3bfb8be2f6
  modified: 2026-10-25T00:22:26.458Z
---

In harbor 0.23.0 and 0.24.0, `Terminus2._query_llm`'s `OutputLengthExceededError` branch returns the
*string* that `TerminusXMLPlainParser.salvage_truncated_response` gives back, where the caller expects
an `LLMResponse`. The next line does `llm_response.content` → `AttributeError: 'str' object has no
attribute 'content'`, which ends the trial. It needs `parser_name="xml"` plus a response that hit
`max_tokens` and still contains a complete `<response>…</response>`, so it hits exp1 TB2.1 evals and
the RL rollouts (both xml), not the json checkpoints. For RL the sample is dropped
(`exception_type` set).

**Why:** found by the client-stack gate's synthetic truncation trial; it is in the pinned reference
stack, so both stacks fail identically and the gate passes — it is a standing production hazard, not
a stack difference.

**How to apply:** if a candidate harbor fixes it, the gate reports it as an outcome difference
("the trial ends differently") — that is the fix showing up, not a regression. See
[[harbor-token-accounting-vs-qwen]].
