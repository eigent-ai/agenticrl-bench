---
name: screening-box-workflow
description: "How to run engine-change screens and own production-recipe runs on the /app SQL-agent GRPO box, and their gotchas"
metadata:
  node_type: memory
  type: reference
  originSessionId: 5dc14ac7-e828-428f-b84f-26ad34dc4d00
  modified: 2026-10-25T00:42:18.333Z
---

The /app box (2x H100) screens rollout-engine changes for the Qwen3.5-2B SQL-agent GRPO recipe (Miles + SGLang).

- `/app/queue/run_screen.sh <change>` runs one queued lr-0 screen (8 steps x 32 prompts, ~18 min incl. ~7 min
  startup) via a root service; dumps land in `/app/runs/screen-<change>/train_data`. One screen at a time;
  `--status` shows progress. Interrupting the client does not stop the screen.
- Own runs (e.g. production recipe lr 1e-6 with dumps) work with
  `HOME=/tmp/x python3 -s /app/queue/run_screen.py <command.txt>` (dump path must be user-writable) but ONLY
  while the service is idle and Ray ports 6379/8265 are free; `ray stop --force` afterwards or the next service
  screen is refused.
- Background Bash tasks die at 2 h: chain at most ~5 screens per task.
- The fidelity check and its rationale live in `/app/fidelity/` (check + NOTES.md); see [[fidelity-check-design]].
