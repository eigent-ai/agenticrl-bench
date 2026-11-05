---
name: falcon-template-mismatch
description: "Falcon-H1R-7B's shipped chat template disagrees with the model; causes systematic OPD KL spikes"
metadata:
  node_type: memory
  type: project
  originSessionId: e12af924-5047-46f1-8151-00ede7f084a4
  modified: 2026-10-24T20:23:12.361Z
---

Measured 2026-10-24 on the box's Falcon-H1R-7B server: the template in /models/Falcon-H1R-7B writes `</think>\n\n`
and ends the current turn with `<|im_end|>` right after the content, but the model writes `</think>\n` and
`\n<|im_end|>` (~-10.5 / -10.8 log-prob otherwise). With a system message the template also renders the last
assistant turn as a past one (off-by-one in its last_query_index), so it must be rendered as the current turn.
The model gives no top-k or generation (gateway refuses), only prefill scoring.

**Why:** these produce ~9-11 nats reverse KL at every end of turn / after `</think>` when scoring in its template.
**How to apply:** if Falcon is used for training, fix its chat template first; don't blame the alignment.
Related: [[live-run-and-testing]].
