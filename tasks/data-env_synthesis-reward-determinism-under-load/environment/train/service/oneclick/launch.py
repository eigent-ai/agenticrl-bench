"""One-click GRPO / rollout launcher for the terminal agent (runs INSIDE the GPU box; here: the pool's training job,
started by /opt/pooltrain/pooltraind.py as the service user on the box's one GPU).

Adapted from OE-S4's launcher (environment/launch/run_terminal_agent.py, Miles 3ad61b8, Qwen3.5-4B colocated, the
64k "survival" layout measured there: GPU 73.7 GiB, host ~228 GiB). Rollouts: mini-swe-agent 2.4.6 (our in-worker
port, examples/terminal_agent) through Miles' in-process Harbor path and the TITO session server; each task container
is a nested Modal sandbox (HARBOR_ENV_TYPE=modal) or comes from the box's sandbox broker.

Two modes, one harness (same prompts, limits, sampling and token path):
  train   GRPO, colocated: Megatron and SGLang share both GPUs (generate, train, push weights)
  rollout --debug-rollout-only: k episodes per task with the base model or a saved HF checkpoint, nothing trained
          (this is `screen` and the TB2.1 evaluation); 2 SGLang engines (DP2); no refill of failed episodes

    cd /root/miles && python /root/oneclick/launch.py --mode train --prompt-data P --out O [--num-rollout 2]
    python /root/oneclick/launch.py ... --print-args          # print the train.py arguments and exit

Plug-in points (all optional): --custom-rm-path (reward from sample.metadata: reward, exit_status, eval_report,
agent_metrics), --custom-generate-function-path / --custom-agent-function-path (episode logic), extra metadata keys
per prompt row (reach the agent function and the reward function), --extra-args (anything else train.py takes).
"""

import json
import os
import shlex
import sys
from dataclasses import dataclass

import typer

from miles.utils.external_utils import command_utils

NUM_GPUS = 2  # default box (2 GPUs); --num-gpus 4 for a 4-GPU rollout box
HARBOR_EXAMPLE = "/root/miles/examples/experimental/harbor"
HARBOR_HOOKS = "/root/miles/examples/swe-agent-harbor-docker"  # reward_func / RolloutFn
BROKER_SOCKET = "/run/sandbox-broker.sock"
MODELS = {  # name -> (HF dir name under model_dir, Miles megatron model type)
    "4b": ("Qwen3.5-4B", "qwen3.5-4B"),
    "2b": ("Qwen3.5-2B", "qwen3.5-2B"),
}


@dataclass
class ScriptArgs(command_utils.ExecuteTrainConfig):
    mode: str = "train"  # train | rollout | convert (HF -> torch_dist into --torch-dist-dir, then exit)
    num_gpus: int = NUM_GPUS
    model: str = "4b"
    model_dir: str = "/models"
    policy_hf: str = ""  # rollout: HF checkpoint to sample from; train: HF checkpoint to start from (default: the base)
    torch_dist_dir: str = ""  # Megatron copy of the base (default: <model_dir>/<name>_torch_dist)
    # trainer layout / memory (OE-S4 64k survival layout)
    tp: int = 2
    cp: int = 1
    max_tokens_per_gpu: int = 8192
    recompute: str = "full"  # full | selective | none
    log_probs_chunk_size: int = 1024
    optimizer_cpu_offload: bool = True
    rollout_gpus_per_engine: int = 0  # 0: train -> 2 (one TP2 engine), rollout -> 1 (two engines)
    sglang_mem_fraction_static: float = 0.7
    colocate_memory_peak_device: str = "cpu"
    sglang_server_concurrency: int = 64  # per engine; also caps concurrent episodes (= task sandboxes)
    sglang_max_mamba_cache_size: int = 0  # >0: cap SGLang's GDN state pool (states, ~50 MB each for 4B) so KV gets the rest
    # GRPO
    lr: float = 1e-6
    eps_clip: float = 0.2
    eps_clip_high: float = 0.28
    filter: str = "no_aborted"  # train: no_aborted | nonzero_std | none
    # workload / episode limits (identical for train and rollout)
    max_seq_len: int = 65536  # tokens per episode: prompt + all turns + observations
    max_response_len: int = 8192  # tokens per model reply
    max_turns: int = 100  # model calls per episode
    command_timeout: int = 120  # s per command; a timeout returns a message to the model
    agent_timeout: int = 14400  # s, Harbor agent-phase safety net (x1); not an episode limit in practice
    trial_timeout: int = 18000  # s, wall-clock cap on one whole trial (setup + agent + tests) in the worker
    command_timeout_cap_by_task: bool = False  # v2 measurement: per-command timeout <= the task's agent timeout_sec
    max_format_errors: int = 3  # consecutive replies without exactly one action before the episode ends
    user_reward_post_process_path: str = ""  # your --custom-reward-post-process-path; wrapped when the wall cap is on
    train_episode_wall_s: int = 0  # v2.5, train only: stop an episode after N s; it stays in its group, excluded from
    #                                the gradient and from GRPO group statistics (examples/terminal_agent/oneclick_hooks.py)
    temperature: float = 1.0
    top_p: float = 1.0
    # run
    prompt_data: str = "/root/oneclick_run/prompts.jsonl"
    out: str = "/root/oneclick_run/out"
    num_rollout: int = 2
    rollout_batch_size: int = 4  # tasks per step (rollout mode: all tasks in prompt_data)
    n_samples_per_prompt: int = 8
    save_interval: int = 1
    save_ckpt: bool = True
    save_rollouts: bool = True
    seed: int = 1
    # harbor
    harbor_env_type: str = ""  # default: sandbox-broker when the broker socket exists, else modal
    harbor_env_kwargs: str = ""
    harbor_tasks_dir: str = "/data/tasks"
    harbor_trials_dir: str = ""  # default: <out>/trials
    harbor_task_map: str = ""  # inbox-rl-v1: JSON {task id: {"path": ...}} for tasks outside --harbor-tasks-dir
    agent_model_name: str = "model"
    modal_config_file: str = os.environ.get("MODAL_CONFIG_PATH", "")
    daytona_api_key_file: str = ""
    e2b_api_key_file: str = ""
    session_server_workers: int = 32
    custom_rm_path: str = "generate.reward_func"
    custom_generate_function_path: str = "miles.rollout.generate_hub.agentic_tool_call.generate"
    custom_agent_function_path: str = "examples.terminal_agent.agent.run"
    rollout_function_path: str = "generate.RolloutFn"  # pool job: pool_canary.CanaryRolloutFn (per-step canary)
    extra_args: str = ""
    print_args: bool = False

    @property
    def dp(self) -> int:
        return self.num_gpus // (self.tp * self.cp)


def check_args(args: ScriptArgs):
    assert args.mode in ("train", "rollout", "convert"), args.mode
    assert args.model in MODELS, args.model
    assert args.num_gpus in (1, 2, 4, 8), args.num_gpus
    assert args.tp in (1, 2) and args.cp in (1, 2) and args.tp * args.cp <= args.num_gpus, (args.tp, args.cp)
    assert args.recompute in ("full", "selective", "none"), args.recompute
    assert args.colocate_memory_peak_device in ("cpu", "gpu"), args.colocate_memory_peak_device
    assert args.filter in ("no_aborted", "nonzero_std", "none"), args.filter
    if not args.rollout_gpus_per_engine:
        args.rollout_gpus_per_engine = 2 if args.mode == "train" else 1
    assert args.rollout_gpus_per_engine in (1, 2), args.rollout_gpus_per_engine
    if not args.harbor_env_type:
        args.harbor_env_type = "sandbox-broker" if os.path.exists(BROKER_SOCKET) else "modal"
    if not args.harbor_trials_dir:
        args.harbor_trials_dir = os.path.join(args.out, "trials")
    _split_user_post_process(args)


def build_train_args(args: ScriptArgs) -> str:
    """The train.py arguments of a run (the job itself is submitted by execute())."""
    name, _ = MODELS[args.model]
    hf = args.policy_hf or f"{args.model_dir}/{name}"
    rollout_mode = args.mode == "rollout"
    if rollout_mode:
        ckpt_args = f"--hf-checkpoint {hf} --debug-rollout-only "
    else:
        ckpt_args = f"--hf-checkpoint {hf} --ref-load {_torch_dist(args)} "
        if args.save_ckpt:
            ckpt_args += (f"--save {args.out}/ckpt --save-interval {args.save_interval} --no-save-optim "
                          f"--save-hf {args.out}/hf/iter_{{rollout_id}} ")
    global_batch = args.rollout_batch_size * args.n_samples_per_prompt
    rollout_args = (
        f"--prompt-data {args.prompt_data} --input-key prompt --metadata-key metadata "
        + ("" if rollout_mode else "--rollout-shuffle ")
        + f"--num-rollout {1 if rollout_mode else args.num_rollout} "
        f"--rollout-batch-size {args.rollout_batch_size} --n-samples-per-prompt {args.n_samples_per_prompt} "
        f"--global-batch-size {global_batch} --balance-data "
        f"--rollout-temperature {args.temperature} --rollout-top-p {args.top_p} "
        f"--rollout-max-response-len {args.max_response_len} --max-seq-len {args.max_seq_len} "
        f"--rollout-seed {args.seed} --seed {args.seed} "
        f"--sglang-server-concurrency {args.sglang_server_concurrency} "
    )
    if args.save_rollouts:
        rollout_args += f"--save-debug-rollout-data {args.out}/rollout/{{rollout_id}}.pt "
    filt = {"no_aborted": "check_no_aborted", "nonzero_std": "check_reward_nonzero_std", "none": ""}[args.filter]
    agent_args = (
        f"--custom-generate-function-path {args.custom_generate_function_path} "
        f"--custom-agent-function-path {args.custom_agent_function_path} "
        f"--custom-rm-path {args.custom_rm_path} --rollout-function-path {args.rollout_function_path} "
        + (f"--dynamic-sampling-filter-path miles.rollout.filter_hub.dynamic_sampling_filters.{filt} "
           if filt and not rollout_mode else "")
        # static ports stay below the sandbox's ephemeral range (16000-65535): a client socket that happens to get
        # one of them as its local port makes the session server refuse to start
        + "--tito-model qwen35 --use-session-server --session-server-port 7100 "
        f"--session-server-workers {args.session_server_workers} --sglang-router-port 7300 "
    )
    grpo_args = (f"--advantage-estimator grpo --entropy-coef 0.00 --eps-clip {args.eps_clip} "
                 f"--eps-clip-high {args.eps_clip_high} ")  # no KL term (add it through --extra-args)
    if args.mode == "train" and args.train_episode_wall_s > 0:
        grpo_args += "--custom-reward-post-process-path examples.terminal_agent.oneclick_hooks.wall_cap_post_process "
    elif args.user_reward_post_process_path:
        grpo_args += f"--custom-reward-post-process-path {args.user_reward_post_process_path} "
    optimizer_args = (
        f"--optimizer adam --lr {args.lr} --lr-decay-style constant --weight-decay 0.1 --adam-beta1 0.9 "
        "--adam-beta2 0.98 "
    )
    if args.optimizer_cpu_offload:
        optimizer_args += "--optimizer-cpu-offload --overlap-cpu-optimizer-d2h-h2d --use-precision-aware-optimizer "
    recompute_args = {
        "full": "--recompute-granularity full --recompute-method uniform --recompute-num-layers 1 ",
        "selective": "--recompute-granularity selective ",
        "none": "",
    }[args.recompute]
    perf_args = (
        f"--tensor-model-parallel-size {args.tp} "
        + ("--sequence-parallel " if args.tp > 1 else "")
        + "--pipeline-model-parallel-size 1 "
        f"--context-parallel-size {args.cp} "
        "--expert-model-parallel-size 1 --expert-tensor-parallel-size 1 "
        + recompute_args
        + "--use-dynamic-batch-size "
        f"--max-tokens-per-gpu {args.max_tokens_per_gpu} "
        f"--log-probs-chunk-size {args.log_probs_chunk_size} "
    )
    sglang_args = (
        f"--rollout-num-gpus-per-engine {args.rollout_gpus_per_engine} "
        f"--sglang-mem-fraction-static {args.sglang_mem_fraction_static} "
        + (f"--sglang-max-mamba-cache-size {args.sglang_max_mamba_cache_size} "
           if args.sglang_max_mamba_cache_size > 0 else "")
    )
    if rollout_mode:
        misc_args = (f"--actor-num-nodes 1 --actor-num-gpus-per-node {args.num_gpus} --num-gpus-per-node {args.num_gpus} "
                     f"--rollout-num-gpus {args.num_gpus} ")
        return f"{ckpt_args}{rollout_args}{agent_args}{sglang_args}{misc_args}{args.extra_args}"
    misc_args = (
        "--attention-dropout 0.0 --hidden-dropout 0.0 "
        "--accumulate-allreduce-grads-in-fp32 --attention-softmax-in-fp32 --attention-backend flash "
        "--colocate "
        f"--colocate-memory-peak-device {args.colocate_memory_peak_device} "
        f"--actor-num-nodes 1 --actor-num-gpus-per-node {args.num_gpus} --num-gpus-per-node {args.num_gpus} "
        f"--rollout-num-gpus {args.num_gpus} "
    )
    return (
        f"{ckpt_args}{rollout_args}{agent_args}{grpo_args}{optimizer_args}{perf_args}{sglang_args}{misc_args}"
        f"{args.extra_args}"
    )


def _split_user_post_process(args: ScriptArgs) -> None:
    """With the wall cap on, a --custom-reward-post-process-path inside --extra-args becomes the wrapped user hook."""
    toks = shlex.split(args.extra_args or "")
    if "--custom-reward-post-process-path" in toks:
        i = toks.index("--custom-reward-post-process-path")
        if args.mode == "train" and args.train_episode_wall_s > 0:
            args.user_reward_post_process_path = args.user_reward_post_process_path or toks[i + 1]
            del toks[i:i + 2]
            args.extra_args = " ".join(shlex.quote(t) for t in toks)


def harbor_env(args: ScriptArgs) -> dict:
    sys.path.insert(0, HARBOR_EXAMPLE)
    from launch_common import harbor_env_vars

    name, _ = MODELS[args.model]
    os.environ["HARBOR_MAX_SEQ_LEN"] = str(args.max_seq_len)
    os.environ["AGENT_MAX_INPUT_TOKENS"] = str(args.max_seq_len)
    os.environ["AGENT_MAX_OUTPUT_TOKENS"] = str(args.max_response_len)
    os.environ["AGENT_TRIAL_TIMEOUT"] = str(args.trial_timeout)
    os.environ.setdefault("HARBOR_TIMEOUT_MULTIPLIER", "1.0")  # verifier / setup: the task's own timeouts
    os.environ.setdefault("HARBOR_ENV_BUILD_TIMEOUT_MULTIPLIER", "2.0")  # first image pulls on Modal
    env = harbor_env_vars(args)
    for var in ("RL_JOB", "RL_SOCKET", "SANDBOX_BROKER_SOCKET"):  # in-box service jobs (rld)
        if os.environ.get(var):
            env[var] = os.environ[var]
    for var, value in os.environ.items():  # the pool job's canary hook (oneclick/pool_canary.py); Harbor telemetry off
        if var.startswith("POOLTRAIN_") or var == "HARBOR_TELEMETRY":
            env[var] = value
    env.update({
        "MSWEA_STEP_LIMIT": str(args.max_turns),
        "MSWEA_COMMAND_TIMEOUT": str(args.command_timeout),
        "MSWEA_COMMAND_TIMEOUT_CAP_BY_TASK": "1" if args.command_timeout_cap_by_task else "0",
        "MSWEA_MAX_FORMAT_ERRORS": str(args.max_format_errors),
        "MSWEA_EPISODE_WALL_S": str(args.train_episode_wall_s if args.mode == "train" else 0),
        "ONECLICK_INNER_REWARD_POST_PROCESS": (args.user_reward_post_process_path
                                               if args.mode == "train" and args.train_episode_wall_s > 0 else ""),
        "MSWEA_MAX_SEQ_LEN": str(args.max_seq_len),
        "MSWEA_MIN_RESPONSE_ROOM": os.environ.get("MSWEA_MIN_RESPONSE_ROOM", "1024"),
        "MSWEA_TOKENIZER_PATH": args.policy_hf or f"{args.model_dir}/{name}",
    })
    if args.harbor_task_map:
        env["HARBOR_TASK_MAP"] = args.harbor_task_map
    return env


def _torch_dist(args: ScriptArgs) -> str:
    name, _ = MODELS[args.model]
    return args.torch_dist_dir or f"{args.model_dir}/{name}_torch_dist"


def prepare(args: ScriptArgs, U):
    name, mtype = MODELS[args.model]
    dst = _torch_dist(args)
    if args.mode in ("train", "convert") and not os.path.exists(os.path.join(dst, "latest_checkpointed_iteration.txt")):
        parent, base = os.path.split(dst.rstrip("/"))
        assert base == f"{name}_torch_dist", f"--torch-dist-dir must end in {name}_torch_dist"
        os.makedirs(parent, exist_ok=True)
        # the base model, or (train --from, inbox-rl-v1) the HF checkpoint the job starts from: fresh optimizer
        U.convert_checkpoint(model_name=name, megatron_model_type=mtype, num_gpus_per_node=1,
                             hf_checkpoint=args.policy_hf or f"{args.model_dir}/{name}", dir_dst=parent)


def execute(args: ScriptArgs):
    U = args.create_backend()
    prepare(args, U)
    if args.mode == "convert":
        return
    os.makedirs(args.out, exist_ok=True)
    os.makedirs(args.harbor_trials_dir, exist_ok=True)
    train_args = build_train_args(args)
    env = harbor_env(args)
    with open(os.path.join(args.out, "launch_args.txt"), "w") as f:
        f.write(" ".join(shlex.quote(a) for a in sys.argv) + "\n\n" + train_args + "\n")
    with open(os.path.join(args.out, "harbor_env.json"), "w") as f:
        json.dump({k: v for k, v in env.items() if "TOKEN" not in k and "SECRET" not in k and "KEY" not in k}, f,
                  indent=1)
    _, mtype = MODELS[args.model]
    U.execute_train(
        train_args=train_args,
        config=args,
        num_gpus_per_node=args.num_gpus,
        megatron_model_type=mtype,
        extra_env_vars={"PYTHONPATH": f"/root/Megatron-LM:{HARBOR_EXAMPLE}:{HARBOR_HOOKS}:/root/miles:"
                                      f"{os.path.dirname(os.path.abspath(__file__))}", **env},
    )


@command_utils.dataclass_cli
def main(args: ScriptArgs):
    check_args(args)
    if args.print_args:
        print(build_train_args(args))
        return
    execute(args)


if __name__ == "__main__":
    typer.run(main)
