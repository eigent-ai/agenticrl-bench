---
name: sql-rl-constraints
description: Ground rules for the Qwen3.5-2B SQL-agent GRPO work on Miles+SGLang (what may and may not be changed)
metadata:
  node_type: memory
  type: project
  originSessionId: 693819a0-56c7-47e9-b47d-c10f431747ae
  modified: 2026-10-25T00:53:03.875Z
---

Miles and SGLang on the box are the stock v0.1.0 release and the user carries no patches on them; every change must
live in their own tree (`/root/miles/examples/sql_agent/...`). The launcher `/app/launch/run_sql_rl.py` is "the recipe"
and must not change — including `--pause-generation-mode in_place`, which their production async job uses.

**Why:** they want to ship the recipe as is and carry it over to the production async job.
**How to apply:** fix things inside `examples/sql_agent/`; for diagnostics, wrap the launcher (e.g. `/root/tools/run_variant.py`
appends flags) instead of editing it. See [[sql-rescue-findings]].
