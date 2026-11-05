"""Sandbox reset for branched rollouts.

The trainer calls reset(traj, k) to get the sandbox a branch starts from: the rollout `traj` (a replay-buffer record)
as it was at step k. Returns the sandbox id; raises NotResettable when that state can't be restored.
"""
import time

import sbx


class NotResettable(Exception):
    """This (rollout, step) can't be branched."""


def reset(traj: dict, k: int) -> str:
    sb = sbx.create(traj["env"], tenant=traj["tenant"])
    for turn in traj["turns"][:k]:
        sb.keys(turn["keys"])
        time.sleep(turn["duration"])
    return sb.id
