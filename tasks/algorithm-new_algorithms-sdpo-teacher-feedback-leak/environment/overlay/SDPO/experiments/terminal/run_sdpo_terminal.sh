#!/bin/bash
# SDPO on the terminal pool. Needs the GPU node (4x H100) and the sandbox fleet for live rollouts.
#   bash experiments/terminal/run_sdpo_terminal.sh [extra hydra overrides]
set -euo pipefail
export TERMINAL_POOL=${TERMINAL_POOL:-/data/sdpo_terminal/pool}
export PYTHONBUFFERED=1
cd /opt/SDPO
python -m verl.trainer.main_ppo --config-name sdpo_terminal "$@"
