# sql2b-0927

- finished: 2026-10-12
- init: in-house chat base (as sql2b-0922)
- SFT: Qwen3.5-9B teacher trajectories, verified only, at most 2 per question, 2,500 rows; full fine-tune, 1 epoch, LR 1e-5 cosine, 64k tokens/step
- RL: Miles v0.1.0 sync GRPO, 60 steps, 8 prompts x 4 samples per step, LR 1e-6, eps-clip 0.2/0.28,
  T=1, 8 turns, 4096 new tokens per turn, 8192 context, thinking off
- RL prompts: `/app/data/sql_train.jsonl` (all SFT trajectories were generated on questions from the same file)
- env: `execute_sql` tool + execution-match reward (`sql_tool.py`, same tool limits as the eval)
- export: HF snapshot of the last step, at `/models/sql2b-0927` on the eval box
- eval dump: `/app/evalsuite/dumps/sql2b-0927.jsonl`
