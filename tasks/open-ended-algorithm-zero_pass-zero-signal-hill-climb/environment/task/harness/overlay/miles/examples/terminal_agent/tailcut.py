"""Straggler cut of a training step (OE task 2 v1.2; train config `rollout_tail_s`, default 0 = off; v1.3: hot-reloadable,
set_tail() at a step start by plugin_hot.RolloutFn from `train.py reload ID --rollout-tail-s S`).

A sync GRPO step waits for its slowest episode, and one episode can stay in a command for up to the per-command cap
(min(600 s, task)) and in the episode for up to the 2400 s episode cap. With ONECLICK_ROLLOUT_TAIL_S = T > 0: once
ONECLICK_TAIL_FRAC (0.9) of the step's episodes are done, the others get at most T more seconds. Then the harness
(mini_swe_agent.py) stops them where they are, a running command or model call included: exit status TailCut, the
tests are not run. Such an episode comes back as a normal sample, flagged here (remove_sample = True,
metadata["tail_cut"] = True), and examples.terminal_agent.plugin_hot.reward_post_process leaves it out of the loss and
out of its group's statistics: it is neither a pass nor a fail (no verdict). Each step logs
`oneclick tail_cut k/n episodes`.
Only episodes that started before the cut was armed are cut (a group Miles starts later, e.g. to replace an aborted
one, runs normally). An episode cut before its first model call makes one 1-token call first, so that it comes back
with a turn (Miles would abort a sample with no model call and re-generate its whole group). A container that is
still starting, or tests that are already running, finish first.

State is per process (the rollout worker runs every episode of a step in one event loop): plugin_hot.RolloutFn calls
start_step() / end_step() around a step, plugin_hot.generate calls episode_started() / episode_finished().
"""

import asyncio
import contextvars
import math
import os
import time

TAIL_S = float(os.environ.get("ONECLICK_ROLLOUT_TAIL_S", "0") or 0)
FRAC = float(os.environ.get("ONECLICK_TAIL_FRAC", "0.9") or 0.9)
STATUS = "TailCut"
_step = {"id": None, "expected": 0, "started": 0, "finished": 0, "deadline": None, "armed_at": None}
_EPISODE_START = contextvars.ContextVar("tailcut_episode_start", default=None)  # set per episode by plugin_hot.generate


class EpisodeTailCut(RuntimeError):
    """The step's straggler cut stopped this episode (not graded; excluded from the loss)."""


def set_tail(seconds) -> None:
    """v1.3: the step's straggler cut in seconds (0 = off); called at a step start, before its first episode."""
    global TAIL_S
    TAIL_S = float(seconds or 0)


def enabled() -> bool:
    return TAIL_S > 0 and _step["id"] is not None


def start_step(step_id: int, expected: int) -> None:
    _step.update(id=step_id, expected=int(expected), started=0, finished=0, deadline=None, armed_at=None)


def end_step() -> None:
    _step.update(id=None, deadline=None, armed_at=None)


def episode_started():
    """Count an episode of the step and remember (in its async context) when it started."""
    _step["started"] += 1
    return _EPISODE_START.set(time.monotonic())


def episode_finished() -> None:
    _step["finished"] += 1
    if enabled() and _step["deadline"] is None and _step["finished"] >= math.ceil(FRAC * max(1, _step["expected"])):
        _step["armed_at"] = time.monotonic()
        _step["deadline"] = _step["armed_at"] + TAIL_S
        print(f"oneclick tail armed: step {_step['id']} {_step['finished']}/{_step['expected']} episodes done, "
              f"the rest get {TAIL_S:.0f} s", flush=True)


def passed() -> bool:
    """True for an episode of this step that started before the cut was armed, once the deadline has passed."""
    d = _step["deadline"]
    if d is None or time.monotonic() < d:
        return False
    started = _EPISODE_START.get()
    return started is None or started < _step["armed_at"]


async def _wait_cut() -> None:
    while not passed():
        await asyncio.sleep(1.0)


async def race(coro):
    """Await `coro`; if the step's tail deadline passes first, cancel it and raise EpisodeTailCut."""
    if not enabled():
        return await coro
    task = asyncio.ensure_future(coro)
    watch = asyncio.ensure_future(_wait_cut())
    try:
        done, _ = await asyncio.wait({task, watch}, return_when=asyncio.FIRST_COMPLETED)
    except BaseException:
        task.cancel()
        watch.cancel()
        raise
    if task in done:
        watch.cancel()
        return task.result()
    task.cancel()
    try:
        await task
    except BaseException:  # noqa: BLE001 - the cancelled call's own error is irrelevant
        pass
    raise EpisodeTailCut("stopped by the step's straggler cut (rollout_tail_s)")


def is_tail_cut(sample) -> bool:
    meta = getattr(sample, "metadata", None) or {}
    return bool(meta.get("tail_cut")) or (meta.get("agent_metrics") or {}).get("mswea_exit_status") == STATUS


def flag(flat) -> list[bool]:
    """Flag the cut samples of a flat sample list (remove_sample = True -> zero loss mask); returns the mask."""
    cut = [is_tail_cut(s) for s in flat]
    for s, c in zip(flat, cut):
        if c:
            s.remove_sample = True
            if s.metadata is not None:
                s.metadata["tail_cut"] = True
    return cut
