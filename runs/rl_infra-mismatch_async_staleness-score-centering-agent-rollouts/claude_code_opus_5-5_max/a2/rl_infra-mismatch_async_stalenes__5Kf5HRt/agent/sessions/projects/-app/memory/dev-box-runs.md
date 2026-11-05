---
name: dev-box-runs
description: "How to run and measure the SQL-agent Miles recipes on the 2xH100 dev box (offline), and its gotchas"
metadata:
  node_type: memory
  type: reference
  originSessionId: 8e4b5fcf-eaa9-4a75-b810-53a9ba3011aa
  modified: 2026-10-25T00:20:22.127Z
---

- `/app/launch/dev_2gpu.sh session|native [flags]` runs a recipe (fp8 SGLang on GPU0, bf16 Megatron TP1 on GPU1),
  saving rollouts to `$DEV/rollouts/<recipe>_<step>.pt`; `LAYOUT=tp2|cp2` replays them on both GPUs. Extra flags
  override the recipe (argparse last wins). Use a fresh `RUN_NAME` per run: `--load` resumes from `$RUN_DIR/$RUN_NAME`.
- TP1 replay on one GPU: `LAYOUT=tp2` plus `--tensor-model-parallel-size 1 --context-parallel-size 1
  --actor-num-gpus-per-node 1 --rollout-num-gpus 1 --num-gpus-per-node 1` (and a matching `--global-batch-size`).
- Point `DEV` at a new dir with a symlink to `~/sc-dev/Qwen3.5-2B_torch_dist` to skip the checkpoint conversion.
- First train step compiles TileLang GDN kernels (~2.5 min); later runs reuse the cache.
- No network: tests using `Qwen/Qwen3-0.6B` from the HF hub fail at collection; run suites with `HF_HUB_OFFLINE=1
  --continue-on-collection-errors` and diff against a pristine copy. For tokenizer tests use `/models/Qwen3.5-2B` with
  `resolve_fixed_chat_template(TITOTokenizerType.QWEN35)` (the native template rejects TITO's suffix render).
- Peak trainer memory: a `--custom-megatron-before-train-step-hook-path` hook that wraps
  `miles.backends.megatron_utils.model.run_forward_backward_pass` and prints `torch.cuda.max_memory_allocated()`.

Related: [[score-centering-sql-agent]]
