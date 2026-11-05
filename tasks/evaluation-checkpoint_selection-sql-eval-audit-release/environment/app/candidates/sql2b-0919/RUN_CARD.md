# sql2b-0919

- finished: 2026-10-11
- init: Qwen/Qwen3.5-2B (15852e8c)
- SFT: trajectory pool: 2,500 rows from our older SQL agents (Qwen2.5-7B-Instruct on the v1 harness with the schema in the prompt, Qwen3-8B thinking on the current harness), every trajectory kept; full fine-tune, 1 epoch, LR 1e-5 cosine, 64k tokens/step
- RL: Miles v0.1.0 sync GRPO, 60 steps, 8 prompts x 4 samples per step, LR 1e-6, eps-clip 0.2/0.28,
  T=1, 8 turns, 4096 new tokens per turn, 8192 context, thinking off
- RL prompts: `/app/data/sql_train.jsonl` (all SFT trajectories were generated on questions from the same file)
- env: `execute_sql` tool + execution-match reward (`sql_tool.py`, same tool limits as the eval)
- export: HF snapshot of the last step, at `/models/sql2b-0919` on the eval box
- eval dump: `/app/evalsuite/dumps/sql2b-0919.jsonl`
