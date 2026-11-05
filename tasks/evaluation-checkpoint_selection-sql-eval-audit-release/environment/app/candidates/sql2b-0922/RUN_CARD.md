# sql2b-0922

- finished: 2026-10-11
- init: in-house chat base: Qwen/Qwen3.5-2B-Base (b1485b2f) + LoRA r=32 on 4,000 general chat turns, merged
- SFT: trajectory pool (same 2,500 rows as sql2b-0919); full fine-tune, 1 epoch, LR 1e-5 cosine, 64k tokens/step
- RL: Miles v0.1.0 sync GRPO, 60 steps, 8 prompts x 4 samples per step, LR 1e-6, eps-clip 0.2/0.28,
  T=1, 8 turns, 4096 new tokens per turn, 8192 context, thinking off
- RL prompts: `/app/data/sql_train.jsonl` (all SFT trajectories were generated on questions from the same file)
- env: `execute_sql` tool + execution-match reward (`sql_tool.py`, same tool limits as the eval)
- export: HF snapshot of the last step, at `/models/sql2b-0922` on the eval box
- eval dump: `/app/evalsuite/dumps/sql2b-0922.jsonl`
