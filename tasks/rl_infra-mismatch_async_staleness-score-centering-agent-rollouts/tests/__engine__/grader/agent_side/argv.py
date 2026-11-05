import runpy
MODEL_ARGS = runpy.run_path("/app/miles/scripts/models/qwen3.5-2B.py")["model_args"]().split()
def build_argv(case: dict, *, tp: int = 1, cp: int = 1, router: str = "127.0.0.1:30777") -> list[str]:
    ip, port = router.split(":")
    argv = list(MODEL_ARGS) + [
        "--hf-checkpoint", "/models/Qwen3.5-2B",
        "--prompt-data", "/dev/null",
        "--input-key", "prompt", "--label-key", "label", "--tool-key", "tools", "--metadata-key", "metadata",
        "--num-rollout", "1",
        "--rollout-batch-size", "32",
        "--n-samples-per-prompt", "4",
        "--global-batch-size", "128",
        "--rollout-max-response-len", "1024",
        "--advantage-estimator", "grpo",
        "--disable-grpo-std-normalization",
        "--use-rollout-logprobs",
        "--calculate-per-token-loss",
        "--loss-type", "score_centering",
        "--rollout-top-logprobs-num", "128",
        "--kl-coef", "0",
        "--entropy-coef", "0",
        "--optimizer", "adam", "--lr", "1e-6", "--lr-decay-style", "constant", "--weight-decay", "0.1",
        "--adam-beta1", "0.9", "--adam-beta2", "0.98",
        "--tensor-model-parallel-size", str(tp),
        "--context-parallel-size", str(cp),
        "--pipeline-model-parallel-size", "1",
        "--use-dynamic-batch-size", "--max-tokens-per-gpu", "8192",
        "--log-probs-chunk-size", "2048",
        "--rollout-num-gpus", "8", "--rollout-num-gpus-per-engine", "1",
        "--sglang-mem-fraction-static", "0.6",
        "--actor-num-nodes", "1", "--actor-num-gpus-per-node", "8",
        "--attention-dropout", "0.0", "--hidden-dropout", "0.0",
        "--accumulate-allreduce-grads-in-fp32", "--attention-softmax-in-fp32",
        "--rollout-temperature", str(case["temperature"]),
        "--rollout-top-p", str(case["top_p"]),
        "--rollout-top-k", str(case["top_k"]),
        "--custom-rm-path", "replay.reward",
    ]
    if tp > 1:
        argv.append("--sequence-parallel")
    if case["recipe"] == "session":
        argv += [
            "--custom-generate-function-path", "miles.rollout.generate_hub.agentic_tool_call.generate",
            "--custom-agent-function-path", "replay.agent",
            "--use-session-server", "v2",
            "--tito-model", "qwen35",
            "--apply-chat-template-kwargs", '{"enable_thinking": false}',
            "--max-seq-len", str(case.get("max_seq_len", 6144)),
            "--sglang-router-ip", "127.0.0.1", "--sglang-router-port", str(case.get("session_port", 31780)),
        ]
    else:
        argv += [
            "--apply-chat-template",
            "--apply-chat-template-kwargs", '{"enable_thinking": false}',
            "--custom-generate-function-path", "miles.rollout.generate_hub.multi_turn.generate",
            "--generate-max-turns", "8",
            "--generate-tool-specs-path", "replay.tool_specs",
            "--generate-execute-tool-function-path", "replay.execute_tool",
            "--generate-tool-call-parser", "qwen3_coder",
            "--rollout-max-context-len", str(case.get("max_context_len", 6144)),
            "--sglang-router-ip", ip, "--sglang-router-port", port,
        ]
    argv += ["--score-centering-is", case["is_mode"]]
    if case["is_mode"] == "tis":
        argv += ["--score-centering-tis-clip", "2"]
    if case["is_mode"] == "mis":
        argv += ["--score-centering-mis-low", "0.5", "--score-centering-mis-high", "5"]
    return argv
