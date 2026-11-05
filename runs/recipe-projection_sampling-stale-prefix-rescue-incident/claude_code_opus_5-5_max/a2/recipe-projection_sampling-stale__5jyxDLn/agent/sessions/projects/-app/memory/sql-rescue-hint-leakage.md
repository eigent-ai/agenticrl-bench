---
name: sql-rescue-hint-leakage
description: "SQL-agent rescue sampler: hinted proposals leak the gold-query hint; feedback loop; what worked and what failed (2026-10-24)"
metadata:
  node_type: memory
  type: project
  originSessionId: 13ae4349-f5f2-41b3-85da-fe20c58217f5
  modified: 2026-10-25T00:01:27.860Z
---

When the gold query was shown to the hinted proposer as a plain hint, about 10% of kept rescue trajectories
mentioned it ("run the suggested query"). Training on them made the student tolerate that text, and leakage grew
to more than 50%. The student then talked about hints in its own rollouts.

- Rewording the hint as a private note cut leakage at base weights to about 2%. One 50-step run stayed clean; a
  replicate still slid back into the loop.
- Final fix: the sampler's `passes()` also rejects any candidate whose assistant text matches `_REFERS_TO_HINT`, a
  regex in `projection.py`. On unhinted rollouts it fires about 1 in 500.

Rejected after testing:
- Full MH with whole-suffix pi/q weights collapsed onto 1-turn faked answers (length bias).
- A length-normalised pi/q score leaked more than the original rule.

**Why:** the length-normalised student score (paper App. C.2) guards against length bias. Even a clean rescue still
trailed plain GRPO over 50 steps (single seed).
**How to apply:** count leaks with /root/diag/leaks.py, not a loose regex; "the query showed" is a false positive.
Test proposal and keep-rule changes offline with /root/diag/sampler_ab.py before running a training job.
Related: [[inplace-push-stale-prefix-cache]]
