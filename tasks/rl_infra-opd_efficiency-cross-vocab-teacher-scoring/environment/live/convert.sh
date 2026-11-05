#!/bin/bash
# Student checkpoint for the Miles step: Qwen3.5-2B HF -> Megatron torch_dist, once per box (root, private network
# namespace, started in the background by box-init). The Miles step waits on the same lock.
set -u
L=/var/lib/live
exec 8>"$L/convert.lock"
flock 8
D=$L/ckpt/Qwen3.5-2B_torch_dist
[ -s "$D/latest_checkpointed_iteration.txt" ] && exit 0
export HOME=$L/engine/home TMPDIR=$L/engine/tmp PYTHONUNBUFFERED=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
export PYTHONPATH=/root/Megatron-LM:/root/miles CUDA_DEVICE_MAX_CONNECTIONS=1 MASTER_ADDR=127.0.0.1 no_proxy=127.0.0.1
mkdir -p "$HOME" "$TMPDIR" "$L/ckpt"
cd /root/miles || exit 2
MA=$(/opt/sglang/bin/python -I -c "import sys; sys.path.insert(0, '/root/miles'); \
from miles.utils.external_utils.model_args_utils import load_model_args; print(load_model_args('qwen3.5-2B'))") || exit 2
rm -rf "$L/ckpt/tmp"
# shellcheck disable=SC2086
/opt/sglang/bin/torchrun --nproc-per-node 1 --master-port 29511 /root/miles/tools/convert_hf_to_torch_dist.py $MA \
  --hf-checkpoint /opt/live/models/Qwen3.5-2B --save "$L/ckpt/tmp" || exit 1
[ -s "$L/ckpt/tmp/latest_checkpointed_iteration.txt" ] || exit 1
mv "$L/ckpt/tmp" "$D"
echo "converted $(date -u +%FT%TZ)"
