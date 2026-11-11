---
name: zero-pass-rl-box
description: "Learnings from the 16h \"learn zero-pass tasks\" Miles/GRPO box (Qwen3.5-4B, plug-in API, rlsdk feedback)"
metadata:
  node_type: memory
  type: project
  originSessionId: d821ad01-a444-41d2-90c8-56dc9f36fa17
  modified: 2026-11-09T07:12:54.449Z
---

Setup seen 2026-11-09: /opt/task (train.py start/reload/status/export, plug-in = plugin.json + algo/ package),
38 never-solved terminal tasks, score = pass@1 of exported checkpoint.

What worked:
- Feedback-conditioned retries: a 2nd user message with rlsdk.feedback text + the earlier attempt's own commands made
  retries pass on tasks plain attempts never pass. Strip the note message tokens ('<|im_start|>user\n{note}<|im_end|>\n')
  from sample.tokens prompt part after the episode (response_length/loss_mask unchanged) -> trains in eval context.
- Override MiniSweAgent._query to insert the note at messages[2] on every call (keeps TITO append-only).
- Generic fixed advice in the note ("remove what you created only for testing") cracked a task (checker re-creates a user).
- "Success replay" notes (commands of an earlier passing run, directive wording) pass ~50%: cheap positive samples.
- Shrinking zero-advantage samples to prompt+1 token in reward_post_process cut log-prob+train from ~4 min to ~40 s.
- rollout_tail_s 150 is safe (passes finish < 200 s); steps ~6-7 min.

What went wrong (avoid):
- GRPO with negative advantages degraded the 4B within ~6 steps both ways: per-sample loss mean -> episode length
  explosion; token-level weighting -> repeated format errors. Positive-only (train passes only) was the stable fix.
- Poison: a turn hitting the 16k reply cap makes the session end the sample there; if the episode passed later, the
  degenerate turn got trained as a pass. Drop TRUNCATED passes; mask turns without exactly one command block.
- Policy-written cause guesses (rlsdk.policy) for retries: 0 passes in 158.

**How to apply:** start positive-only from step 0 with these filters; keep hooks fail-safe (exceptions crash the run).
