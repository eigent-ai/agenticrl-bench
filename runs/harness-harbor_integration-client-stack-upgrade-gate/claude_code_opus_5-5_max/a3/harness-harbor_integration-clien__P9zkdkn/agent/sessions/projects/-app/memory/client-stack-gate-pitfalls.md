---
name: client-stack-gate-pitfalls
description: Non-obvious traps found while building and testing the harbor+litellm client-stack gate in /app/gate
metadata:
  node_type: memory
  type: project
  originSessionId: dab471cc-f58e-4f22-b1da-45812a5dd94e
  modified: 2026-11-10T18:55:36.771Z
---

The client-stack gate (/app/gate/check.sh) replays Terminus-2 trials through two harbor+litellm venvs on a virtual-time asyncio loop. Traps that cost hours (2026-11-10):

- This box (and CI, "like this one") runs gVisor: loopback TCP connects, bytes and closes are delivered asynchronously, and select() can report a socket writable before epoll does. An event loop that jumps its clock "when idle" must count in-flight connects/bytes/closes at the socket layer (vtloop.py), or replays become load-dependent and flaky.
- litellm's acompletion runs the sync completion() in an executor thread for every call; track run_in_executor before jumping time.
- Terminus2.__init__ keyword defaults (e.g. proactive_summarization_threshold=8000, tmux_pane_width=160) override the Terminus2Options Field defaults; editing only the Field default is a no-op (bit our mutant tests twice).
- Reference harbor 0.24.0 crashes with AttributeError when it salvages a truncated XML reply (_query_llm returns a str). That is reference behaviour the gate must preserve, not a gate bug.
- Pooled keep-alive connections leak across scenarios run in one process; the runner forks a fresh process per scenario and binds a fresh server port each time.

**Why:** each looked like a gate bug or a candidate difference and took long to diagnose.
**How to apply:** when changing the gate's replay machinery, re-run its stress test (many parallel copies of one scenario must agree) and the mutant suite before trusting verdicts. Related: [[client-stack-gate-design]].
