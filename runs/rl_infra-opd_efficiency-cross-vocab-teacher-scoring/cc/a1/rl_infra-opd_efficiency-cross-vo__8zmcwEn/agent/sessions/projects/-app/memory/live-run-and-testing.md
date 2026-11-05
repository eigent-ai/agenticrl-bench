---
name: live-run-and-testing
description: How /opt/live/run.sh behaves on the OPD box and how to test the terminal_opd teacher hooks without pytest
metadata:
  node_type: memory
  type: project
  originSessionId: e12af924-5047-46f1-8151-00ede7f084a4
  modified: 2026-10-24T20:23:08.362Z
---

`/opt/live/run.sh` snapshots /app/miles when it starts, replays mswea/terminus_think/sql through the hooks against the
box's Falcon-H1R-7B teacher (gateway :30000 in front of SGLang :30010), then runs one Miles OPD step; only the latest
completed run is kept (with a code digest). Any code edit after a run's snapshot needs a re-run. With per-turn
scoring (2026-10-24) it took ~18 min (scoring ~8 min at opd_teacher_concurrency 32).

**Why:** the user keeps that run as the deliverable, so it must reflect the final code.
**How to apply:** finish code changes first, then run it once in the background and watch its log.

Testing: pytest is not installed in /opt/agentpy; run `python examples/terminal_opd/test_teacher_scoring.py`
directly. `/app/tools/fake_teacher.py` gives exact, prefix-dependent log-probs for checking the token sequences sent.
Findings and design are in /app/NOTES.md; see [[falcon-template-mismatch]].
