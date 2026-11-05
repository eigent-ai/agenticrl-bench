---
name: rescue-eval-method
description: How to evaluate SQL-agent RL runs reliably on this box (in-run eval is too noisy)
metadata:
  node_type: memory
  type: reference
  originSessionId: 899210cc-9d6a-4ccc-8ca6-13bd419d22ae
  modified: 2026-10-24T22:03:53.649Z
---

- In-run eval (2 samples/question, 96 hard + 64 regular) swings ±5 points between runs with identical weights.
- Reliable comparison: convert the step-49 torch_dist ckpt (`tools/convert_torch_dist_to_hf.py` + 
  `/app/scratch/complete_hf_ckpt.py` to add vision/MTP tensors), then `/app/scratch/serve_and_eval.sh <hf_dir> <gpu>
  <port> <out.json> 8` (8 samples/question, fresh cache namespace per request).
- Same data order in every run (seed 1), so per-step training pass rate of the student's own samples is a paired
  comparison: `/app/scratch/paired_pass.py`.
- `/app/scratch/diag_launch.py` wraps the launcher and adds `--save-debug-train-data` (trainer log-probs per sample);
  `DIAG_EXTRA` env appends flags for diagnostic runs only.

Related: [[rescue-experiment-2026-10]]
