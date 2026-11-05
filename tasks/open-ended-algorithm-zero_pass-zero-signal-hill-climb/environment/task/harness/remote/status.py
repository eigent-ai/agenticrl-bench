"""Progress of a one-click run (runs in the GPU sandbox, prints one JSON line). Stdlib only.

    python3 status.py <run_dir> [--total N]
Counts: Harbor trials finished / running (trial dirs under <run_dir>/out/trials), end reasons, console markers
(train / update_weights ends, Harbor trial verdict lines, tracebacks, OOM), launcher alive, GPU and host memory.
"""
import ast
import collections
import glob
import json
import os
import re
import subprocess
import sys
import time

RUN = sys.argv[1]
TOTAL = int(sys.argv[sys.argv.index("--total") + 1]) if "--total" in sys.argv else None
OUT = os.path.join(RUN, "out")
CONSOLE = os.path.join(RUN, "console.log")


def _literal(text: str) -> dict:
    """A logged metrics dict -> dict (nan / inf become None)."""
    return ast.literal_eval(re.sub(r"(?<![\w'])-?(nan|inf)(?![\w'])", "None", text))


def end_reason(res: dict) -> str:
    exc = (res.get("exception_info") or {}).get("exception_type") or ""
    meta = ((res.get("agent_result") or {}).get("metadata") or {})
    ms = meta.get("mswea_exit_status") or ""
    if exc in ("AgentTimeoutError",):
        return "timeout"
    if exc == "EpisodeWallCapped" or ms == "WallCapped":
        return "wall_capped"
    if exc and not res.get("verifier_result"):
        return f"error:{exc}"
    return {"Submitted": "submitted", "LimitsExceeded": "step_limit", "ContextLimitExceeded": "context_limit",
            "RepeatedFormatError": "format_error", "ModelError": "model_error"}.get(ms, f"other:{ms or exc}")


def main():
    st = {"t": time.time()}
    trials = sorted(glob.glob(os.path.join(OUT, "trials", "*")))
    done, running, reasons, rewards = 0, [], collections.Counter(), []
    for d in trials:
        if not os.path.isdir(d):
            continue
        rp = os.path.join(d, "result.json")
        if os.path.exists(rp):
            try:
                res = json.load(open(rp))
            except Exception:  # noqa: BLE001 - being written
                running.append(d)
                continue
            if not res.get("finished_at"):
                running.append(d)
                continue
            done += 1
            reasons[end_reason(res)] += 1
            vr = res.get("verifier_result") or {}
            rw = (vr.get("rewards") or {}).get("reward")
            if rw is not None:
                rewards.append(float(rw))
        else:
            running.append(d)
    st.update({"trial_dirs": len(trials), "done": done, "running": len(running), "end_reasons": dict(reasons),
               "n_reward": len(rewards), "mean_reward": round(sum(rewards) / len(rewards), 4) if rewards else None})
    now = time.time()
    ages = []
    for d in running:
        try:
            ages.append(now - os.path.getctime(d))
        except OSError:
            pass
    if ages:
        st["running_age_s"] = {"max": round(max(ages)), "median": round(sorted(ages)[len(ages) // 2])}
    if TOTAL is not None:
        st["total"] = TOTAL
    try:
        text = open(CONSOLE, errors="replace").read()
    except OSError:
        text = ""
    st["console_bytes"] = len(text)
    st["train_end"] = len(re.findall(r"Timer train end", text))
    st["update_weights_end"] = len(re.findall(r"Timer update_weights end", text))
    st["verdict_lines"] = len(re.findall(r"Harbor trial \S+: exit_status=", text))
    st["trial_fail_lines"] = len(re.findall(r"Harbor trial for \S+ (failed|exceeded)", text))
    st["tracebacks"] = text.count("Traceback (most recent call last)")
    wc = re.findall(r"oneclick wall_capped (\d+)/(\d+) episodes", text)
    if wc:
        st["wall_capped_per_step"] = [f"{a}/{b}" for a, b in wc]
    st["oom"] = len(re.findall(r"out of memory|OutOfMemoryError|Tried to allocate", text))
    m = re.findall(r"step (\d+): (\{'train/loss'.*?\})", text)
    if m:
        try:
            last = _literal(m[-1][1])
            st["last_step"] = {"step": int(m[-1][0]), **{k: last.get(k) for k in
                               ("train/loss", "train/pg_loss", "train/grad_norm", "train/pg_clipfrac",
                                "train/train_rollout_logprob_abs_diff")}}
        except Exception:  # noqa: BLE001
            pass
    r = re.findall(r"rollout (\d+): (\{'rollout/response_lengths'.*?\})", text)
    if r:
        try:
            last = _literal(r[-1][1])
            st["last_rollout"] = {"rollout": int(r[-1][0]), **{k: last.get(k) for k in
                                  ("rollout/raw_reward", "rollout/response_lengths", "rollout/total_lengths",
                                   "rollout/truncated")}}
        except Exception:  # noqa: BLE001
            pass
    lp = subprocess.run("pgrep -f '[o]neclick/launch.py' | head -1", shell=True, capture_output=True, text=True)
    st["launcher_alive"] = bool(lp.stdout.strip())
    tp = subprocess.run("pgrep -f '[t]rain.py' | head -1", shell=True, capture_output=True, text=True)
    st["train_py_alive"] = bool(tp.stdout.strip())
    g = subprocess.run("nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits", shell=True,
                       capture_output=True, text=True)
    st["gpu_mib"] = [int(x) for x in g.stdout.split()] if g.returncode == 0 else None
    for f in ("/sys/fs/cgroup/memory.current", "/sys/fs/cgroup/memory/memory.usage_in_bytes"):
        if os.access(f, os.R_OK):
            st["host_gib"] = round(int(open(f).read()) / 2**30, 1)
            break
    try:
        peak = 0
        for line in open(os.path.join(RUN, "host.csv")):
            parts = line.split()
            if len(parts) == 2:
                peak = max(peak, int(parts[1]))
        st["host_peak_gib"] = round(peak / 2**30, 1)
    except (OSError, ValueError):
        pass
    print(json.dumps(st))


if __name__ == "__main__":
    main()
