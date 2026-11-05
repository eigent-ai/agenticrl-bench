#!/bin/bash
# One Miles OPD training step of the Qwen3.5-2B student (colocated, Megatron) on <step dir>/0.pt: the replayed
# episodes with the hooks' teacher_log_probs (--load-debug-rollout-data, so no rollout engine). Root (started by
# run.sh). Ray runs with token authentication (RAY_AUTH_MODE=token, token in a root-only file) on free ports, its temp
# dir root-only, so nobody else on the box can submit work to it.
#   miles_step.sh <step dir>
set -u
S=$1
L=/var/lib/live
exec 8>"$L/convert.lock"
flock 8   # the student checkpoint (box-init converts it in the background)
D=$L/ckpt/Qwen3.5-2B_torch_dist
[ -s "$D/latest_checkpointed_iteration.txt" ] || { echo "student checkpoint missing"; exit 3; }
exec 8>&-
N=$(cat "$S/n_samples")
export PATH=/opt/sglang/bin:/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export HOME=$S/home TMPDIR=$S/tmp PYTHONUNBUFFERED=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 no_proxy=127.0.0.1
RT=$L/ray   # short: Ray's socket paths must fit in 107 bytes
rm -rf "$RT"; mkdir -p "$HOME" "$TMPDIR" "$RT"
umask 077
head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n' > "$HOME/ray_token"
export RAY_AUTH_MODE=token RAY_AUTH_TOKEN_PATH=$HOME/ray_token
cd /root/miles || exit 2
MA=$(python -I -c "import sys; sys.path.insert(0, '/root/miles'); \
from miles.utils.external_utils.model_args_utils import shell_safe_model_args; print(shell_safe_model_args('qwen3.5-2B'))") || exit 2
read -r GCS DASH < <(python -I -c "import socket
ps = []
for _ in range(2):
    s = socket.socket(); s.bind(('127.0.0.1', 0)); ps.append(s)
print(*[s.getsockname()[1] for s in ps])")
ray start --head --node-ip-address 127.0.0.1 --port "$GCS" --num-gpus 1 --disable-usage-stats --temp-dir "$RT" \
  --include-dashboard true --dashboard-host 127.0.0.1 --dashboard-port "$DASH" > "$S/ray_start.log" 2>&1 || exit 4
ENVJ='{"env_vars": {"PYTHONPATH": "/root/Megatron-LM:/root/miles", "CUDA_DEVICE_MAX_CONNECTIONS": "1",
  "PYTHONUNBUFFERED": "1", "NCCL_NVLS_ENABLE": "0", "MASTER_ADDR": "127.0.0.1", "no_proxy": "127.0.0.1",
  "HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1"}}'
ARGS="--hf-checkpoint /opt/live/models/Qwen3.5-2B --ref-load $D \
--load-debug-rollout-data $S/{rollout_id}.pt --disable-rollout-global-dataset \
--num-rollout 1 --rollout-batch-size $N --n-samples-per-prompt 1 --global-batch-size $N \
--rollout-max-response-len 2048 --rollout-temperature 1 \
--use-opd --opd-type sglang --opd-kl-coef 1.0 \
--advantage-estimator grpo --entropy-coef 0.00 --eps-clip 0.2 --eps-clip-high 0.28 \
--optimizer adam --lr 1e-6 --lr-decay-style constant --weight-decay 0.1 --adam-beta1 0.9 --adam-beta2 0.98 \
$(cat /opt/live/step.args 2>/dev/null) \
--tensor-model-parallel-size 1 --pipeline-model-parallel-size 1 --context-parallel-size 1 \
--expert-model-parallel-size 1 --expert-tensor-parallel-size 1 \
--recompute-granularity full --recompute-method uniform --recompute-num-layers 1 \
--use-dynamic-batch-size --max-tokens-per-gpu 8192 --log-probs-chunk-size 1024 \
--attention-dropout 0.0 --hidden-dropout 0.0 --accumulate-allreduce-grads-in-fp32 --attention-softmax-in-fp32 \
--attention-backend flash \
--colocate --actor-num-nodes 1 --actor-num-gpus-per-node 1 --num-gpus-per-node 1 --rollout-num-gpus 1 \
--save-debug-train-data $S/train_{rollout_id}_{rank}.pt"
# shellcheck disable=SC2086
ray job submit --address "http://127.0.0.1:$DASH" --runtime-env-json "$ENVJ" -- python3 /root/miles/train.py $MA $ARGS
rc=$?
ray stop --force > /dev/null 2>&1
exit $rc
