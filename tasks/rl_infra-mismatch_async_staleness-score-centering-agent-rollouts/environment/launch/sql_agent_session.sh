#!/bin/bash
# Recipe R1: SQL agent through the session server (v2, TITO), fp8 SGLang sampler, top-p/top-k sampling,
# score centering + TIS. Usage (on the cluster): RUN_NAME=sql-sc-session bash /app/launch/sql_agent_session.sh
source "$(dirname "$0")/common.sh"

ROLLOUT_ARGS=(
  --rollout-temperature 1.0
  --rollout-top-p 0.95
  --rollout-top-k 64
  --custom-generate-function-path miles.rollout.generate_hub.agentic_tool_call.generate
  --custom-agent-function-path examples.sql_agent.agent.run_agent
  --custom-rm-path examples.sql_agent.sql_tool.reward_func
  --use-session-server v2
  --tito-model qwen35
  --apply-chat-template-kwargs '{"enable_thinking": false}'
  --max-seq-len 6144
)

IS_ARGS=(
  --score-centering-is tis
  --score-centering-tis-clip 2
)

python3 train.py \
  "${MODEL_ARGS[@]}" "${CKPT_ARGS[@]}" "${DATA_ARGS[@]}" "${ROLLOUT_ARGS[@]}" "${LOSS_ARGS[@]}" "${IS_ARGS[@]}" \
  "${OPT_ARGS[@]}" "${PERF_ARGS[@]}" "${SGLANG_ARGS[@]}" "${CLUSTER_ARGS[@]}" "${MISC_ARGS[@]}" "$@"
