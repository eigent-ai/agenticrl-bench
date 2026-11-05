---
name: live-run-tool
description: "/opt/live/run.sh live Qwen job semantics: kept run is tied to the exact /app/terminal_rl tree; busy ports"
metadata:
  node_type: memory
  type: reference
  originSessionId: 6704db28-84ee-4c36-bef8-76c1584552a3
  modified: 2026-10-24T21:12:39.292Z
---

`/opt/live/run.sh` starts the team's live job, or follows it if one is already running. The job is 8 TMax episodes ×
3 agents, Qwen3-4B on the box's H100, with the proxy run from /app/terminal_rl as user agent. It prints a summary and
writes the proxy log to /tmp/live-proxy.log.

**The last finished run is kept only for the exact /app/terminal_rl tree hash.** Any later file change there, including
`__pycache__` written by tests, needs a new run. So run tests and replays with PYTHONDONTWRITEBYTECODE=1 and do the
live run last.

Ports on the box:
- 30000 is the live engine gateway (`/generate`, `/abort_request`).
- 31000 is the real SGLang engine (auth-protected).
- 40000+ are per-run gateways.

Use other ports, e.g. 39100+, for fake_sglang replays. Related: [[agent-proxy-rewrite]].
