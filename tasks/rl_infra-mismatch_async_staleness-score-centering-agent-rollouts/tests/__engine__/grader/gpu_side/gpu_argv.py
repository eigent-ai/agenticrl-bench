from argv import build_argv
SC_ONLY = ("--rollout-top-logprobs-num", "--score-centering-is", "--score-centering-tis-clip",
           "--score-centering-mis-low", "--score-centering-mis-high")
def _set(argv, flag, value):
    i = argv.index(flag)
    return argv[: i + 1] + [value] + argv[i + 2:]
def to_baseline(argv):
    out, i = [], 0
    while i < len(argv):
        if argv[i] in SC_ONLY:
            i += 2
            continue
        out.append("policy_loss" if argv[i] == "score_centering" and out and out[-1] == "--loss-type" else argv[i])
        i += 1
    if "policy_loss" not in out:
        raise ValueError("no --loss-type score_centering in the recipe command line")
    return out
def build_gpu_argv(case: dict, *, tp: int, cp: int, ckpt: str, baseline: bool = False) -> list[str]:
    argv = build_argv(case, tp=tp, cp=cp)
    argv = _set(argv, "--actor-num-gpus-per-node", str(tp * cp))
    argv += [
        "--ref-load", ckpt, "--load", "/nonexistent/sc-gpu-run",
        "--debug-disable-optimizer",
        "--recompute-granularity", "full", "--recompute-method", "uniform", "--recompute-num-layers", "1",
        "--attention-backend", "flash",
    ]
    return to_baseline(argv) if baseline else argv
