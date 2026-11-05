"""Training-time hooks of the one-click harness (v2.5).

wall_cap_post_process(args, samples) -> (raw_rewards, normalized_rewards)       (--custom-reward-post-process-path)
  Per-episode wall cap for GRPO training (launch.py --train-episode-wall-s N; never used by rollout/measure runs).
  An episode that reaches the cap is stopped by the agent (exit status WallCapped, no verifier run) and comes back as
  a normal, non-ABORTED sample, so Miles keeps its group (an ABORTED sample would make Miles re-generate the whole
  group). Here such a sample is a neutral cut, not a reward-0 episode:
    * excluded from its group's GRPO statistics: mean / std over the group's uncapped samples only;
    * advantage 0 and sample.remove_sample = True, so its loss mask is zeroed (no gradient, not in the token count);
    * a group whose samples are all capped (or that has a single uncapped one) contributes nothing.
  Everything else is Miles' default GRPO normalization (rewards - group mean, / (std + 1e-6) with
  --grpo-std-normalization). The per-step count is logged as `oneclick wall_capped k/n episodes`.

Composing with your own reward post-process (Miles takes ONE --custom-reward-post-process-path):
  (a) wrap: give launch.py --user-reward-post-process-path my_mod.fn (or keep --custom-reward-post-process-path in
      --extra-args; launch.py moves it). wall_cap_post_process then flags the capped samples FIRST
      (remove_sample = True, metadata["wall_capped"] = True), calls my_mod.fn(args, samples) on the full, unchanged
      sample list, and forces the capped samples' advantage to 0. Your hook should leave them out of its statistics:
      test is_wall_capped(sample) (or use live_mask / grpo_normalize_excluding below).
  (b) helper: inside your own hook call `mask = flag_wall_capped(samples)` and, for GRPO-style stats,
      `grpo_normalize_excluding(args, flat_samples, raw_rewards, mask)`; return 0 advantage for masked samples.
"""

import importlib
import logging
import math
import os
from collections import defaultdict

logger = logging.getLogger(__name__)
CAPPED = "WallCapped"


def is_wall_capped(sample) -> bool:
    meta = getattr(sample, "metadata", None) or {}
    if meta.get("wall_capped"):
        return True
    return ((meta.get("agent_metrics") or {}).get("mswea_exit_status") == CAPPED)


def _flat(samples):
    return [s for g in samples for s in g] if samples and isinstance(samples[0], list) else list(samples)


def live_mask(samples) -> list[bool]:
    """True for every sample that was NOT wall-capped (flattened order)."""
    return [not is_wall_capped(s) for s in _flat(samples)]


def flag_wall_capped(samples) -> list[bool]:
    """Flag capped samples (remove_sample = True -> zero loss mask; metadata['wall_capped'] = True). Returns the
    capped mask in flattened order. Idempotent."""
    capped = [is_wall_capped(s) for s in _flat(samples)]
    for s, c in zip(_flat(samples), capped):
        if c:
            s.remove_sample = True
            if s.metadata is not None:
                s.metadata["wall_capped"] = True
    return capped


def grpo_normalize_excluding(args, flat, raw, capped) -> list[float]:
    """Miles' GRPO normalization per prompt group over the uncapped samples only; capped samples get 0."""
    est = getattr(args, "advantage_estimator", "grpo")
    if not (est in ("grpo", "gspo", "reinforce_plus_plus_baseline") and getattr(args, "rewards_normalization", True)):
        return [0.0 if c else r for r, c in zip(raw, capped)]
    groups = defaultdict(list)
    for i, s in enumerate(flat):
        key = s.group_index if getattr(s, "group_index", None) is not None else i // max(1, args.n_samples_per_prompt)
        groups[key].append(i)
    norm = [0.0] * len(flat)
    std_norm = est in ("grpo", "gspo") and getattr(args, "grpo_std_normalization", True)
    for idx in groups.values():
        live = [i for i in idx if not capped[i]]
        if not live:
            continue
        mean = sum(raw[i] for i in live) / len(live)
        std = math.sqrt(sum((raw[i] - mean) ** 2 for i in live) / (len(live) - 1)) if len(live) > 1 else 0.0
        for i in live:
            v = raw[i] - mean
            if std_norm and len(live) > 1 and std > 0:
                v = v / (std + 1e-6)
            norm[i] = v
    return norm


def _inner_hook():
    path = os.getenv("ONECLICK_INNER_REWARD_POST_PROCESS", "").strip()
    if not path:
        return None
    mod, _, fn = path.rpartition(".")
    return getattr(importlib.import_module(mod), fn)


def wall_cap_post_process(args, samples):
    flat = _flat(samples)
    capped = flag_wall_capped(samples)
    inner = _inner_hook()
    if inner is not None:  # (a) wrap the user's hook: capped samples flagged first, their advantage forced to 0
        raw, norm = inner(args, samples)
        norm = [0.0 if c else float(v) for v, c in zip(list(norm), capped)]
    else:
        raw = [s.get_reward_value(args) for s in flat]
        norm = grpo_normalize_excluding(args, flat, raw, capped)
    n = sum(capped)
    logger.info(f"oneclick wall_capped {n}/{len(flat)} episodes")
    print(f"oneclick wall_capped {n}/{len(flat)} episodes", flush=True)
    return raw, norm


# ---- v1.2: live config (train.py set RUN lr=X) -------------------------------------------------------------------
# --custom-megatron-before-train-step-hook-path examples.terminal_agent.oneclick_hooks.live_cfg_hook
# Runs on every trainer rank before each optimizer step. When $T1_LIVE_CFG (JSON written by train.py set) has a new
# "lr", it becomes the scheduler's max lr (the recipe's lr schedule is constant, so it holds from this step on) and the
# lr of every param group for this step. Rank 0 appends {"rollout_id", "step_id", "lr", "utc"} to $T1_LIVE_APPLIED.
_LIVE = {"mtime": None, "lr": None}


def live_cfg_hook(args, rollout_id, step_id, model, optimizer, opt_param_scheduler):
    import json
    import time

    path = os.environ.get("T1_LIVE_CFG")
    if not path:
        return
    try:
        mtime = os.stat(path).st_mtime
    except OSError:
        return
    if mtime == _LIVE["mtime"]:
        return
    _LIVE["mtime"] = mtime
    try:
        lr = json.loads(open(path).read()).get("lr")
    except Exception as e:  # noqa: BLE001
        logger.warning(f"oneclick live cfg unreadable: {e!r}")
        return
    if lr is None or float(lr) == _LIVE["lr"]:
        return
    lr = float(lr)
    sch = opt_param_scheduler
    if sch is not None:
        sch.max_lr = lr
        if getattr(sch, "init_lr", None) is not None and sch.init_lr > lr:
            sch.init_lr = lr
        if getattr(sch, "min_lr", None) is not None and sch.min_lr > lr:
            sch.min_lr = lr
    groups = getattr(optimizer, "param_groups", None) or []
    for g in groups:
        if "max_lr" in g:
            g["max_lr"] = lr
        if "min_lr" in g and g["min_lr"] > lr:
            g["min_lr"] = lr
        g["lr"] = lr * g.get("lr_mult", 1.0)
    _LIVE["lr"] = lr
    try:
        import torch.distributed as dist
        rank0 = not dist.is_initialized() or dist.get_rank() == 0
    except Exception:  # noqa: BLE001
        rank0 = True
    if rank0:
        msg = {"rollout_id": int(rollout_id), "step_id": int(step_id), "lr": lr, "param_groups": len(groups),
               "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        print(f"oneclick live lr -> {lr} at rollout {rollout_id}", flush=True)
        out = os.environ.get("T1_LIVE_APPLIED")
        if out:
            with open(out, "a") as f:
                f.write(json.dumps(msg) + "\n")
