---
name: hint-strip-plugin
description: "What worked in the zero-pass GRPO plug-in (note stripping, reflections, zero-adv shrinking, replay) and pitfalls hit"
metadata:
  node_type: memory
  type: project
  originSessionId: 32ba8245-e6b9-4a68-9d53-c7880513befe
  modified: 2026-10-27T16:50:45.065Z
---

Plug-in at /app/algo (2026-10-27 session), run `hint1`.

- Zero-advantage sample shrinking (cut to prompt + 1 masked token in reward_post_process) cut training from ~425 s
  to ~110 s per step with identical gradients — the single biggest time win.
- Reflection via rlsdk.policy.chat only works if the episode is given as a transcript inside ONE user message with
  a reviewer system prompt; feeding the raw agent conversation makes the policy keep emitting bash commands.
  Use only the policy's own messages (no command outputs) to stay inside the allowed-context rules.
- miles WeightVersionSpan is a frozen dataclass (fields abs_start/abs_end): rebuild with dataclasses.replace.
- Bash tool default timeout is 120 s: pass `timeout` for longer sleeps when polling runs.
- First passes appeared at step 2 (one hinted with a reflection note, one plain).

**Why:** hard-won during a 16 h session. **How to apply:** start from these when building a similar plug-in; see
[[zero-pass-rl-box]].

Reasoning-collapse lesson (same session): mixing note-conditioned (stripped) and plain episodes in ONE GRPO group made
plain failures get negative advantages whenever noted siblings passed; within ~6 steps the policy's reasoning per reply
fell ~4x and episodes ballooned to the call/context limits. Fix: normalize plain and noted episodes separately and mask
all reasoning tokens of noted samples. Track mean reasoning chars/reply of plain episodes per step as a health metric.

Outcome (2026-10-28): shipped hint3 iter 44 (chain hint1->hint2->hint3). eval.py on it, k=8: 5 tasks at 5-7/8, one at
1/8 -> ~0.095 pass@1 over 38 (base 0). What worked in the end: separate plain/noted normalization, ALL noted reasoning
masked, KL 0.05 + --calculate-per-token-loss, priority sampling toward tasks with plain passes, solution notes.
