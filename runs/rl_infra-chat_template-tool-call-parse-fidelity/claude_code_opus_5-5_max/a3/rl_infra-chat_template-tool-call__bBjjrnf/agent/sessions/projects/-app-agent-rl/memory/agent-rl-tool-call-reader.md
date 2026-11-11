---
name: agent-rl-tool-call-reader
description: "State of the agent-RL tool-call fix (handed over 2026-11-11) and the user's constraints for changes to the rollout loop"
metadata:
  node_type: memory
  type: project
  originSessionId: bb4284c4-f090-47c0-ad63-87b6aefd7156
  modified: 2026-11-11T13:12:29.248Z
---

On 2026-11-11 the loop's tool-call parsing was replaced by examples/tool_agent/tool_calls.py (ToolCallReader); the
final live run was run 2 (tree e7083683...). Findings, judgement calls and numbers are in /app/NOTES.md.

**Why:** the user requires that training runs exactly the calls the model made in its own format (never reasoning
drafts or unfinished calls, arguments as written) while samples, tokens, loss masks and rewards otherwise stay the
same; it must hold for every model in launch/run_tool_agent.py's table, with per-model settings only in the table or
the loop, and the loop / launcher interfaces unchanged.

**How to apply:** a new policy model needs a reader for its SGLang tool-call parser in tool_calls.py (the loop raises
otherwise) and `python tests/test_tool_calls.py`; check loop changes with old-vs-new replays of data/runs (identical
samples wherever calls are unchanged). See [[live-box-tooling]].
