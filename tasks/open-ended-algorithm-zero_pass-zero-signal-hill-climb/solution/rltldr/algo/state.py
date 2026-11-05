"""Per-job plug-in state under <job>/out/algo_state (rlsdk.paths.job_out(); one node, flock'ed appends).

- feedback buffer: per task, sanitized checker reports of failed episodes (seeded from the base model's screening
  reports in /data/eval, then the policy's own failures);
- chains: per task, the RLTL;DR attempt chains (insights so far, attempt number);
- ledger.jsonl: one line per finished episode.
"""
from __future__ import annotations

import fcntl
import hashlib
import io
import json
import tarfile
import time
from contextlib import contextmanager
from pathlib import Path

from rlsdk.paths import job_out

from algo.config import CFG
from algo.tail import tail_from_messages

ROOT = job_out() / "algo_state"
KEEP_PER_TASK = 12


@contextmanager
def locked(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(path) + ".lock", "a+") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lk, fcntl.LOCK_UN)


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().splitlines():
        try:
            rows.append(json.loads(line))
        except ValueError:
            pass
    return rows


def append(path: Path, row: dict) -> None:
    with locked(path):
        with open(path, "a") as f:
            f.write(json.dumps(row, sort_keys=True) + "\n")


def safe(task_id: str) -> str:
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in task_id)


def _screening_tails() -> dict:
    """trial -> tail of the base model's screening trajectory (the ones shipped in /data/eval)."""
    out = {}
    p = Path(CFG.get("seed_trajectories") or "")
    if not p.is_file():
        return out
    try:
        with tarfile.open(p) as tf:
            for m in tf.getmembers():
                if m.isfile() and m.name.endswith("mini_trajectory.json"):
                    trial = m.name.split("/")[-2]
                    msgs = json.load(io.TextIOWrapper(tf.extractfile(m))).get("messages") or []
                    out[trial] = tail_from_messages(msgs)
    except (OSError, ValueError, tarfile.TarError):
        pass
    return out


def ensure_seeded() -> None:
    """Load the base model's screening reports once per job; later calls are no-ops."""
    path = Path(CFG.get("seed_feedback") or "")
    marker = ROOT / "seeded"
    if not path.is_file() or marker.exists():
        return
    with locked(ROOT / "seed"):
        if marker.exists():
            return
        tails = _screening_tails()
        n = 0
        for r in read_jsonl(path):
            add_feedback(r["task_id"], r["text"], int(r.get("n_passed") or 0), -1, "screen",
                         {"trial": r.get("trial"), "tail": tails.get(r.get("trial") or "", "(not available)")})
            n += 1
        marker.write_text(str(n))


def add_feedback(task_id: str, text: str, n_passed: int, step: int, source: str, extra: dict | None = None) -> None:
    append(ROOT / "feedback" / f"{safe(task_id)}.jsonl",
           {"t": time.time(), "step": step, "n_passed": n_passed, "source": source,
            "sha": hashlib.sha256(text.encode()).hexdigest()[:16], "text": text, **(extra or {})})


def pick_feedback(task_id: str, key: str) -> dict | None:
    """One of the 3 most informative recent failures (most checks passed, then newest), chosen by `key`."""
    rows = read_jsonl(ROOT / "feedback" / f"{safe(task_id)}.jsonl")[-KEEP_PER_TASK:]
    if not rows:
        return None
    seen, uniq = set(), []
    for r in reversed(rows):
        if r["sha"] not in seen:
            seen.add(r["sha"])
            uniq.append(r)
    uniq.sort(key=lambda r: (-int(r.get("n_passed", 0)), -float(r.get("t", 0))))
    top = uniq[:3]
    return top[int(hashlib.sha256(key.encode()).hexdigest(), 16) % len(top)]


def log_episode(row: dict) -> None:
    append(ROOT / "ledger.jsonl", {"t": time.time(), **row})
