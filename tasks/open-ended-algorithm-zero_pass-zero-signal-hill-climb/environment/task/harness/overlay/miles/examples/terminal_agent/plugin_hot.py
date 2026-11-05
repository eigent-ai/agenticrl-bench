"""Hot-reloadable algorithm plug-in of a train run (OE task 2 v1.2, + v1.3 hot settings). A train run always gives Miles these entry points:

  --custom-generate-function-path    examples.terminal_agent.plugin_hot.generate
  --custom-agent-function-path       examples.terminal_agent.plugin_hot.run          (and .abort)
  --custom-reward-post-process-path  examples.terminal_agent.plugin_hot.reward_post_process
  --rollout-function-path            examples.terminal_agent.plugin_hot.RolloutFn

Each one calls the matching hook of the run's ACTIVE plug-in version, or the default when that version has none
(Miles' agentic_tool_call.generate, the harness's examples.terminal_agent.agent.run, Miles' group-normalized GRPO).

The active version is <run>/plugin_active.json (scripts/train.py start / reload write it; RL_PLUGIN_RUN_DIR names the
run dir): {"version": k, "dir": <snapshot dir or null>, "sha256": ..., "manifest": <its plugin.json>}. RolloutFn reads
it once per step, before the step's first episode. On a new version it drops every `algo` / `algo.*` module, replaces
the old snapshot dir on sys.path with the new one and imports the new hooks. That version then serves the whole step:
its episodes, its generate and its reward post-process. Ray, SGLang and Megatron keep running. If the import fails,
the previous version stays active. Each switch (or failure) is appended to <run>/plugin_applied.jsonl together with
the step it took effect at. Module-level state of the old version is gone after a switch (keep state on disk, e.g.
under rlsdk.paths.job_out() / "algo_state").
Loss flags (plugin.json miles_args) are Miles arguments, parsed once when the run starts: they are NOT reloadable.
A new version's own generate add_arguments flags that the run does not have yet get their defaults.

v1.3: the run's hot settings (train.py reload ID --lr X --rollout-tail-s S) work the same way. <run>/hot_config.json
holds the requested version {"version": j, "lr": ..., "rollout_tail_s": ...}. RolloutFn reads it once per step, before
the step's first episode, freezes it for that step in <run>/hot_step/<step>.json, applies rollout_tail_s to the step's
straggler cut (tailcut.set_tail) and appends a row to <run>/config_applied.jsonl when the version changes. The lr is
applied to that step's optimizer step by examples/terminal_agent/hot_lr.py in the Megatron ranks, which read the
same hot_step file.
"""

import argparse
import importlib
import inspect
import json
import logging
import os
import sys
import time
from pathlib import Path

from examples.terminal_agent import tailcut

logger = logging.getLogger(__name__)
RUN_DIR = Path(os.environ.get("RL_PLUGIN_RUN_DIR") or "/nonexistent-plugin-run")
DEFAULTS = {"generate": "miles.rollout.generate_hub.agentic_tool_call.generate",
            "agent_function": "examples.terminal_agent.agent.run",
            "reward_post_process": ""}
_state = {"active": None, "hooks": None, "announced": set(), "failed": set()}


def _load(path: str):
    mod, _, name = path.rpartition(".")
    return getattr(importlib.import_module(mod), name)


def _as_generate(fn):
    """Miles' calling convention for a generate function (compatibility.load_generate_function)."""
    from miles.rollout.inference_rollout.compatibility import LegacyGenerateFnAdapter, _is_legacy_generate_fn

    if inspect.isclass(fn):
        return fn()
    return LegacyGenerateFnAdapter(fn) if _is_legacy_generate_fn(fn) else fn


def _read_active() -> dict:
    try:
        return json.loads((RUN_DIR / "plugin_active.json").read_text())
    except (OSError, ValueError):
        return {"version": 0, "dir": None, "sha256": None, "manifest": {}}


def _activate(active: dict) -> None:
    """Import one version's hooks: drop every algo / algo.* module, swap the snapshot dir on sys.path, import."""
    for name in [m for m in sys.modules if m == "algo" or m.startswith("algo.")]:
        del sys.modules[name]
    for d in {(_state["active"] or {}).get("dir"), active.get("dir")} - {None}:
        while d in sys.path:
            sys.path.remove(d)
    if active.get("dir"):
        sys.path.insert(0, active["dir"])
    importlib.invalidate_caches()
    man = active.get("manifest") or {}
    _state["active"] = active
    hooks = {k: (_load(man.get(k) or d) if (man.get(k) or d) else None) for k, d in DEFAULTS.items()}
    hooks["generate"] = _as_generate(hooks["generate"])
    _state["hooks"] = hooks


def _ensure() -> dict:
    if _state["hooks"] is None:
        _activate(_read_active())
    return _state["hooks"]


def _record(rec: dict) -> None:
    rec["utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        with open(RUN_DIR / "plugin_applied.jsonl", "a") as f:
            f.write(json.dumps(rec) + "\n")
    except OSError:
        pass
    print(f"[plugin] {json.dumps(rec)}", flush=True)


def _fill_new_flags(args, gen) -> None:
    own = getattr(gen, "add_arguments", None)
    if not callable(own) or args is None:
        return
    scratch = argparse.ArgumentParser(add_help=False)
    own(scratch)
    for act in scratch._actions:
        if act.dest and act.dest != "help" and not hasattr(args, act.dest):
            setattr(args, act.dest, act.default)


def maybe_reload(step: int, args=None) -> None:
    """At a step boundary: switch to the active plug-in version if it changed; record when each version took effect."""
    _ensure()
    prev, active = _state["active"], _read_active()
    v = active.get("version")
    if v != prev.get("version") and v not in _state["failed"]:
        try:
            _activate(active)
            _fill_new_flags(args, _state["hooks"]["generate"])
        except Exception as e:  # noqa: BLE001 - keep training with the previous version
            _state["failed"].add(v)
            _record({"version": v, "sha256": active.get("sha256"), "ok": False, "step": step,
                     "error": f"{type(e).__name__}: {e}"[:1500], "kept_version": prev.get("version")})
            _activate(prev)
    cur = _state["active"]
    if cur.get("version") not in _state["announced"]:
        _state["announced"].add(cur.get("version"))
        _record({"version": cur.get("version"), "sha256": cur.get("sha256"), "ok": True, "effective_step": step})


_hot = {"version": None}


def maybe_hot_config(step: int) -> dict | None:
    """At a step start: freeze the run's hot settings for this step (hot_step/<step>.json), apply the tail cut."""
    try:
        cfg = json.loads((RUN_DIR / "hot_config.json").read_text())
    except (OSError, ValueError):
        return None
    rec = {"config_version": cfg.get("version"), "lr": cfg.get("lr"), "rollout_tail_s": cfg.get("rollout_tail_s")}
    try:
        (RUN_DIR / "hot_step").mkdir(exist_ok=True)
        tmp = RUN_DIR / "hot_step" / f".{step}.json.tmp"
        tmp.write_text(json.dumps(rec))
        tmp.replace(RUN_DIR / "hot_step" / f"{step}.json")
    except OSError:
        pass
    if rec["rollout_tail_s"] is not None:
        tailcut.set_tail(rec["rollout_tail_s"])
    if rec["config_version"] != _hot["version"]:
        _hot["version"] = rec["config_version"]
        row = {**rec, "effective_step": step, "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        try:
            with open(RUN_DIR / "config_applied.jsonl", "a") as f:
                f.write(json.dumps(row) + "\n")
        except OSError:
            pass
        print(f"[hot] config v{rec['config_version']} from step {step}: lr {rec['lr']}, rollout_tail_s "
              f"{rec['rollout_tail_s']}", flush=True)
    return rec


# ---- the entry points Miles calls -----------------------------------------------------------------------------------
async def generate(input):
    hooks = _ensure()
    token = tailcut.episode_started()
    try:
        return await hooks["generate"](input)
    finally:
        tailcut.episode_finished()
        tailcut._EPISODE_START.reset(token)


def _add_arguments(parser) -> None:
    """Flags of the default generate plus the starting version's own (Miles registers them once, at start)."""
    default = _load(DEFAULTS["generate"])
    if callable(getattr(default, "add_arguments", None)):
        default.add_arguments(parser)
    gen = _ensure()["generate"]
    own = getattr(gen, "add_arguments", None)
    if callable(own) and gen is not default:
        scratch = argparse.ArgumentParser(add_help=False)
        own(scratch)
        have = set(parser._option_string_actions)
        for act in scratch._actions:
            if act.option_strings and not set(act.option_strings) & have:
                parser._add_action(act)


generate.add_arguments = _add_arguments


async def run(*a, **k):
    return await _ensure()["agent_function"](*a, **k)


async def abort(args) -> None:
    fn = _ensure()["agent_function"]
    hook = getattr(sys.modules.get(getattr(fn, "__module__", ""), None), "abort", None)
    if callable(hook) and hook is not abort:
        await hook(args)


def reward_post_process(args, samples):
    from examples.terminal_agent import oneclick_hooks as H

    flat = H._flat(samples)
    cut = tailcut.flag(flat)
    n = sum(cut)
    if tailcut.TAIL_S > 0:
        print(f"oneclick tail_cut {n}/{len(flat)} episodes", flush=True)
    hook = _ensure()["reward_post_process"]
    if hook is not None:  # the plug-in's own; cut samples keep advantage 0 whatever it returns
        raw, norm = hook(args, samples)
        return raw, [0.0 if c else float(v) for v, c in zip(list(norm), cut)]
    if n:
        raw = [s.get_reward_value(args) for s in flat]
        return raw, H.grpo_normalize_excluding(args, flat, raw, cut)
    from miles.ray.rollout.train_data_conversion import _post_process_rewards

    return _post_process_rewards(args, samples, custom_reward_post_process_func=None)


def _rollout_base():
    from generate import RolloutFn as base  # examples/swe-agent-harbor-docker (the harness's rollout function)

    return base


class RolloutFn(_rollout_base()):
    """The harness's rollout function; at each train step's start: plug-in version check, hot settings (lr for this
    step's optimizer step, rollout_tail_s), then the straggler cut."""

    async def _call_train(self, input):
        args = self.state.args
        maybe_reload(input.rollout_id, args)
        maybe_hot_config(input.rollout_id)
        tailcut.start_step(input.rollout_id, args.rollout_batch_size * args.n_samples_per_prompt)
        try:
            return await super()._call_train(input)
        finally:
            tailcut.end_step()
