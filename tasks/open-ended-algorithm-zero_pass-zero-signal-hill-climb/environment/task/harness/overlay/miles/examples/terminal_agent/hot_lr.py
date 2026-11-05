"""Hot-reloadable learning rate of a train run (OE task 2 v1.3; `train.py reload ID --lr X`).

Miles calls `before_train_step` (--custom-megatron-before-train-step-hook-path, set by harness/remote/launch.py for
every train run) in every Megatron rank right before each optimizer step's forward/backward. The lr for train step k
is the one plugin_hot.RolloutFn froze for that step when its rollout started: <run>/hot_step/<k>.json (written once,
before the step's first episode, so every rank reads the same value). When it differs from the scheduler's lr, the
hook rescales the scheduler's max / min lr and every param group's lr / max_lr / min_lr by the same factor (any
per-group multiplier is kept). Megatron's scheduler then keeps that lr
in its own step(). Rank 0 appends <run>/lr_applied.jsonl and prints `[hot] lr ...`. Nothing else of the optimizer
(Adam moments, weight decay) changes. Imports nothing heavy (runs in the Megatron actors).
"""

import json
import os
import time
from pathlib import Path

RUN_DIR = Path(os.environ.get("RL_PLUGIN_RUN_DIR") or "/nonexistent-plugin-run")
_last = {"step": None, "lr": None}


def _step_lr(rollout_id: int):
    """The lr frozen for this step, or the latest earlier one (None: no hot config yet)."""
    d = RUN_DIR / "hot_step"
    for k in range(int(rollout_id), -1, -1):
        p = d / f"{k}.json"
        if p.exists():
            try:
                return float(json.loads(p.read_text())["lr"]), k
            except (OSError, ValueError, KeyError, TypeError):
                return None, None
        if k < int(rollout_id) - 1000:
            break
    return None, None


def _rank() -> int:
    try:
        import torch.distributed as dist

        return dist.get_rank() if dist.is_available() and dist.is_initialized() else 0
    except Exception:  # noqa: BLE001
        return 0


def _set_group_lr(sched, pg, f) -> None:
    """The group's current lr: scaled by f (keeps any per-group multiplier), or from the scheduler."""
    old = pg.get("lr")
    lr = float(old) * f if (f is not None and old is not None) else sched.get_lr(pg)
    if hasattr(old, "fill_"):
        pg["lr"].fill_(lr)
    else:
        pg["lr"] = lr


def before_train_step(args, rollout_id, step_id, model, optimizer, opt_param_scheduler) -> None:
    if optimizer is None or opt_param_scheduler is None:
        return
    want, src = _step_lr(rollout_id)
    if want is None:
        return
    sched = opt_param_scheduler
    cur = float(sched.max_lr)
    if cur > 0 and abs(want - cur) <= 1e-12 * max(abs(cur), 1.0):
        return
    f = want / cur if cur > 0 else None
    groups = list(getattr(optimizer, "param_groups", []) or [])
    sched.max_lr = want
    if f is not None:
        sched.min_lr = float(sched.min_lr) * f
        if getattr(sched, "init_lr", None) is not None:
            sched.init_lr = min(float(sched.init_lr) * f, want)
    for pg in groups:
        for key in ("max_lr", "min_lr"):
            if key in pg and pg[key] is not None and f is not None:
                pg[key] = float(pg[key]) * f
        _set_group_lr(sched, pg, f)
    args.lr = want
    if _rank() == 0:
        lrs = sorted({round(float(pg["lr"]), 12) for pg in groups if "lr" in pg})
        rec = {"step": int(rollout_id), "train_step": int(step_id), "lr_before": cur, "lr": want, "from_hot_step": src,
               "param_groups": len(groups), "group_lrs": lrs[:4], "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        try:
            with open(RUN_DIR / "lr_applied.jsonl", "a") as fh:
                fh.write(json.dumps(rec) + "\n")
        except OSError:
            pass
        print(f"[hot] lr {cur:g} -> {want:g} at step {rollout_id} ({len(groups)} param groups, lr now {lrs[:4]})",
              flush=True)
