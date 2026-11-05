---
name: session-timeline
description: Session start time and deadline for the TB2.1 RL task (16h budget on 4xH200)
metadata:
  node_type: memory
  type: project
  originSessionId: adaac65c-6c0c-465b-a136-27b2873bacf6
  modified: 2026-10-27T05:20:02.146Z
---

Session started 2026-10-27 05:20 UTC. 16h budget -> hard deadline ~21:20 UTC.
Plan to have final checkpoint exported to /app/checkpoint and all jobs stopped by ~20:45 UTC.

**Why:** the task gives 16 hours total; GPU jobs need 10-12 min startup each.
**How to apply:** check `date` against this when planning restarts / evals. See [[tb21-rl-plan]].
