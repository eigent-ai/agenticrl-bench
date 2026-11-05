#!/bin/bash
# Local runs of our two recipes on this dev box (2x H100), with the flags of sql_agent_session.sh / sql_agent_native.sh
# (model, sampling, loss, IS, per-GPU batching) and only the cluster-sized settings scaled down:
#   bash /app/launch/dev_2gpu.sh session|native [extra Miles flags...]
# LAYOUT=split (default): the fp8 SGLang sampler on GPU 0, the bf16 Megatron trainer at TP1 on GPU 1; NUM_ROLLOUT
#   (default 2) rollout + train steps of 4 prompts x 4 samples from /data/sql_agent/train.jsonl; each step's rollout
#   data is saved to $DEV/rollouts/<recipe>_<step>.pt. The engine quantizes the checkpoint to fp8 when it loads it and
#   this SGLang build cannot take the trainer's bf16 weight pushes into it, so locally the sampler keeps the
#   checkpoint's weights (--debug-skip-weight-update: from the second step on the rollouts are stale, off-policy).
# LAYOUT=tp2 | cp2: the trainer alone on both GPUs at TP2 or CP2, on the rollout data a split run saved
#   (--load-debug-rollout-data; no sampler).
# The first run converts /models/Qwen3.5-2B to a Megatron torch_dist checkpoint in $DEV (a few minutes).
set -euo pipefail
RECIPE=${1:?usage: dev_2gpu.sh session|native [extra Miles flags...]}
shift
case "$RECIPE" in session | native) ;; *) echo "recipe must be session or native" >&2; exit 2 ;; esac
DEV=${DEV:-$HOME/sc-dev}
LAYOUT=${LAYOUT:-split}
mkdir -p "$DEV/rollouts" "$DEV/runs"
cd /app/miles
export PYTHONPATH="/root/Megatron-LM:/app/miles${PYTHONPATH:+:$PYTHONPATH}" CUDA_DEVICE_MAX_CONNECTIONS=1
CK="$DEV/Qwen3.5-2B_torch_dist"
if [ ! -s "$CK/latest_checkpointed_iteration.txt" ]; then
  MA=( $(python3 -c 'import runpy; print(runpy.run_path("scripts/models/qwen3.5-2B.py")["model_args"]())') )
  rm -rf "$CK.tmp"
  CUDA_VISIBLE_DEVICES=0 torchrun --nproc-per-node 1 --master-port 29531 tools/convert_hf_to_torch_dist.py \
    "${MA[@]}" --hf-checkpoint /models/Qwen3.5-2B --save "$CK.tmp"
  mv "$CK.tmp" "$CK"
fi
DEV_ARGS=(
  --ref-load "$CK"
  --num-rollout "${NUM_ROLLOUT:-2}" --rollout-batch-size 4 --n-samples-per-prompt 4 --global-batch-size 16
  --save-interval 1000000 --num-gpus-per-node 2
  --reward-key score  # examples.sql_agent.sql_tool.reward_func returns {"score", "pred", "acc"}
  --session-server-workers 2  # session recipe: 2 session servers are plenty for 16 conversations
)
case "$LAYOUT" in
  split)
    DEV_ARGS+=(--rollout-num-gpus 1 --rollout-num-gpus-per-engine 1 --actor-num-nodes 1 --actor-num-gpus-per-node 1
               --tensor-model-parallel-size 1 --context-parallel-size 1 --debug-skip-weight-update
               --save-debug-rollout-data "$DEV/rollouts/${RECIPE}_{rollout_id}.pt") ;;
  tp2 | cp2)
    [ "$LAYOUT" = tp2 ] && PAR=(--tensor-model-parallel-size 2 --context-parallel-size 1) \
                        || PAR=(--tensor-model-parallel-size 1 --context-parallel-size 2)
    DEV_ARGS+=(--colocate --rollout-num-gpus 2 --actor-num-nodes 1 --actor-num-gpus-per-node 2 "${PAR[@]}"
               --load-debug-rollout-data "$DEV/rollouts/${RECIPE}_{rollout_id}.pt") ;;
  *) echo "LAYOUT must be split, tp2 or cp2" >&2; exit 2 ;;
esac
export RUN_DIR="$DEV/runs" RUN_NAME="${RUN_NAME:-dev-$RECIPE-$LAYOUT}"
exec bash "/app/launch/sql_agent_$RECIPE.sh" "${DEV_ARGS[@]}" "$@"
