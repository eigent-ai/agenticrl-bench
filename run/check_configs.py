"""Compare the job configs the run scripts print with the job configs Harbor recorded for the released runs.

    python3 -I check_configs.py [--release DIR] [--extra-records DIR ...] [--verbose]

For every recorded job config.json it finds, it runs the class script of that task with --print-config (cached per
task and agent; nothing is launched, no credential is read) and diffs the two JobConfigs, apart from job_name,
jobs_dir and the task path (Harbor records a task as "tasks" or as a one-task "datasets" folder).

- Oracle and no-op validation runs (validation/<task>/{oracle,nop}, validation/rerun-20261110): must be identical.
- Released model runs (runs/, open_ended/runs/, and --extra-records folders of raw units): every difference must be
  one of the explained kinds below; anything else is UNEXPECTED. The released runs used private adapters around
  Harbor's built-in agents (subscription, gateway or Vertex logins); a public run uses the built-in agent with an API
  key, so those fields differ by construction.

Agent environment values are never printed: a value shows as ${NAME} (a template) or <literal>.
Exit 0 if there is nothing unexpected.
"""

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("taskinfo", RUN_DIR / "taskinfo.py")
taskinfo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(taskinfo)

SCRIPT = {"verifiable": "run_verifiable.sh", "broker": "run_broker.sh", "open-ended": "run_open_ended.sh"}
# Hosts of the released runs' private model access. The release's redaction writes the private model gateway as
# internal-host.invalid or <redacted-host>; where a record still names a private host (the gateway, or the API proxy
# of the early Grok Build runs), it is matched by the SHA-256 of its name, so the name itself is not in these scripts.
REDACTED_GATEWAY = {"internal-host.invalid", "<redacted-host>"}
PRIVATE_GATEWAY_SHA256 = {"d04863b5e9c64a94deab733220f42fc0281d6706eb2cdef28dbf20bc03e0114f"}
PRIVATE_PROXY_SHA256 = {"1cdb8837eb68eefa12e470ad6736ea05046de8efdbd8a85c10e283bdecdf1a46"}
VERTEX_HOSTS = {"aiplatform.googleapis.com", "oauth2.googleapis.com"}  # Vertex AI and its login


def _sha(host: str) -> str:
    return hashlib.sha256(host.encode()).hexdigest()


def is_gateway(host: str) -> bool:
    return host in REDACTED_GATEWAY or _sha(host) in PRIVATE_GATEWAY_SHA256


def is_private(host: str) -> bool:
    return is_gateway(host) or _sha(host) in PRIVATE_PROXY_SHA256 or host in VERTEX_HOSTS


def shown(hosts) -> list[str]:
    """Hosts for printing: a private host shows as <private host>."""
    return [h if h in VERTEX_HOSTS or not is_private(h) else "<private host>" for h in hosts]


META_HOSTS = {"dev.meta.ai", "api.meta.ai", "lookaside.facebook.com"}  # added to the shared list once Muse ran
# Hosts that left task.toml at v1 and come from the launch for model agents (rollout-time [agent] allowlists).
NESTED = {
    "harness-harbor_integration-harbor-upgrade-row-parity": {"api.modal.com", "*.w.modal.host"},
    "data-env_synthesis-reward-determinism-under-load": {"api.modal.com", "*.w.modal.host", "app.daytona.io",
                                                         "*.daytona.io", "s3.us-east-1.amazonaws.com"},
}
BUILTIN = {"claude_code": "claude-code", "codex": "codex", "antigravity": "antigravity-cli", "grok_build": "grok-build",
           "muse": "muse-code"}
WHY = {
    "agent adapter": "agents[].name: a private adapter (<module>:<Class>) around this built-in agent",
    "agent login": "agents[].env: the private adapter's own login variables, or the key as a literal; a public run passes ${KEY}",
    "agent hosts": "agents[].extra_allowed_hosts: the private gateway/proxy/Vertex hosts instead of the provider's API",
    "gateway host": "environment.extra_allowed_hosts: the private model gateway, not needed by a public run",
    "meta hosts": "environment.extra_allowed_hosts: the 3 Meta hosts, added to the shared list after the first runs",
    "nested hosts": "nested-sandbox hosts that task.toml listed when the runs were made and the launch adds since v1",
    "proxy model name": "agents[].model_name: an API proxy's prefix (<proxy>/<model>)",
    "grok wait": "background_wait_sec: unset (Harbor default 600 s) in the first Grok Build runs, 27000 s after",
    "grok subagents": "grok_config: subagent_model_inheritance, set in the Grok Build re-runs and by these scripts",
    "claude version": "version: the Claude Code CLI version, pinned by these scripts; the first runs installed it unpinned",
    "muse effort": "reasoning_effort: the Muse Code runs recorded ultra, which their CLIs (1.4.13, 1.4.14) do not offer "
                   "and ran as xhigh (agent/muse-code.stderr.log); these scripts pass xhigh",
}
GROK_CONFIG = {"features": {"subagent_model_inheritance": True}}
CLAUDE_VERSION = {"cc": "2.1.310", "ccf": "2.1.321"}


def mask_env(env: dict) -> dict:
    return {k: (v if re.fullmatch(r"\$\{[A-Za-z0-9_]+(:-[^}]*)?\}", str(v)) else "<literal>") for k, v in env.items()}


def normalize(cfg: dict) -> dict:
    cfg = json.loads(json.dumps(cfg))
    for k in ("job_name", "jobs_dir"):
        cfg.pop(k, None)
    for k in ("tasks", "datasets"):
        if k in cfg:
            cfg.pop(k)
            cfg["task"] = "<task path>"
    for a in cfg.get("agents", []):
        if "env" in a:
            a["env"] = mask_env(a["env"])
    return cfg


def printed(release: Path, task_dir: Path, cls: str, agent: str, cache: dict) -> dict:
    key = (task_dir.name, agent)
    if key not in cache:
        out = subprocess.run(["bash", str(RUN_DIR / SCRIPT[cls]), str(task_dir), "/nonexistent/jobs", "--agent",
                              agent, "--print-config"], capture_output=True, text=True)
        if out.returncode != 0:
            sys.exit(f"{SCRIPT[cls]} {task_dir.name} --agent {agent} --print-config failed:\n{out.stderr}")
        cache[key] = json.loads(out.stdout)
    return cache[key]


def agent_key(cfg: dict, hint: str | None) -> str:
    a = cfg["agents"][0]
    name, model = a["name"], a.get("model_name") or ""
    if name in ("oracle", "nop"):
        return name
    if "antigravity" in name:
        return "agyc" if "carbon" in model else "agy"
    if "claude_code" in name and "fable" in model:
        return "ccf"
    for frag, key in (("claude_code", "cc"), ("codex", "codex"), ("grok_build", "grok"), ("muse", "muse")):
        if frag in name:
            return key
    return hint or name


def diff(rec: dict, ours: dict, task: str, agent: str) -> tuple[list[str], list[str]]:
    """Returns (explained kinds, unexpected lines)."""
    kinds, bad = [], []
    ra, oa = rec.pop("agents", [{}]), ours.pop("agents", [{}])
    re_, oe = rec.get("environment", {}), ours.get("environment", {})
    rh, oh = re_.pop("extra_allowed_hosts", []), oe.pop("extra_allowed_hosts", [])
    nested = next((h for t, h in NESTED.items() if task.endswith(t)), set()) if agent not in ("oracle", "nop") else set()
    # environment hosts
    extra_rec, extra_ours = [h for h in rh if h not in oh], [h for h in oh if h not in rh]
    if all(is_gateway(h) for h in extra_rec) and set(extra_ours) <= META_HOSTS | nested:
        kinds += ["gateway host"] * bool(extra_rec) + ["meta hosts"] * bool(set(extra_ours) & META_HOSTS)
        kinds += ["nested hosts"] * bool(set(extra_ours) & nested)
        if [h for h in rh if h in oh] != [h for h in oh if h in rh]:
            bad.append(f"environment.extra_allowed_hosts: same hosts, other order: {shown(rh)} vs {shown(oh)}")
    else:
        bad.append(f"environment.extra_allowed_hosts: recorded only {shown(extra_rec)}, printed only {shown(extra_ours)}")
    # the rest of the job
    if rec != ours:
        for k in sorted(set(rec) | set(ours)):
            if rec.get(k) != ours.get(k):
                bad.append(f"{k}: recorded {json.dumps(rec.get(k))} printed {json.dumps(ours.get(k))}")
    # the agent
    r, o = dict(ra[0]), dict(oa[0])
    adapter = ":" in r.get("name", "")  # a private adapter <module>:<Class>
    if r.get("name") != o.get("name"):
        frag = next((f for f in BUILTIN if f in r.get("name", "")), None)
        if ":" in r.get("name", "") and frag and BUILTIN[frag] == o.get("name"):
            kinds.append("agent adapter")
        else:
            bad.append(f"agents[].name: recorded {r.get('name')} printed {o.get('name')}")
    r.pop("name", None), o.pop("name", None)
    if r.get("model_name") != o.get("model_name"):
        rm = str(r.get("model_name", ""))
        if adapter and "/" in rm and rm.split("/", 1)[1] == o.get("model_name"):
            kinds.append("proxy model name")
        else:
            bad.append(f"agents[].model_name: recorded {r.get('model_name')} printed {o.get('model_name')}")
    r.pop("model_name", None), o.pop("model_name", None)
    rk, ok = dict(r.pop("kwargs", {}) or {}), dict(o.pop("kwargs", {}) or {})
    if agent in CLAUDE_VERSION and "version" not in rk and ok.get("version") == CLAUDE_VERSION[agent]:
        kinds.append("claude version"); ok.pop("version")
    if agent == "grok" and "grok_config" not in rk and ok.get("grok_config") == GROK_CONFIG:
        kinds.append("grok subagents"); ok.pop("grok_config")
    if agent == "grok" and "background_wait_sec" not in rk and ok.get("background_wait_sec") == 27000:
        kinds.append("grok wait"); ok.pop("background_wait_sec")
    if agent == "muse" and rk.get("reasoning_effort") == "ultra" and ok.get("reasoning_effort") == "xhigh":
        kinds.append("muse effort"); rk.pop("reasoning_effort"); ok.pop("reasoning_effort")
    if rk != ok:
        bad.append(f"agents[].kwargs: recorded {rk} printed {ok}")
    renv, oenv = r.pop("env", {}) or {}, o.pop("env", {}) or {}
    if renv != oenv:
        # the adapter's own login variables (or the key as a literal) vs the one ${KEY} template of a public run
        if adapter and len(oenv) <= 1 and all(v.startswith("${") for v in oenv.values()):
            kinds.append("agent login")
        else:
            bad.append(f"agents[].env: recorded {renv} printed {oenv}")
    rah, oah = r.pop("extra_allowed_hosts", []) or [], o.pop("extra_allowed_hosts", []) or []
    if rah != oah:
        xr, xo = [h for h in rah if h not in oah], [h for h in oah if h not in rah]
        proxy = bool(xr) and all(is_private(h) for h in xr)
        if all(is_private(h) for h in xr) and (not xo or proxy or set(xo) <= nested):
            kinds.append("agent hosts")
            kinds += ["nested hosts"] * bool(set(xo) & nested)
        else:
            bad.append(f"agents[].extra_allowed_hosts: recorded only {shown(xr)}, printed only {shown(xo)}")
    if r != o:
        bad.append(f"agents[] other fields: recorded {r} printed {o}")
    return sorted(set(kinds)), bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", default=str(RUN_DIR.parent))
    ap.add_argument("--extra-records", action="append", default=[],
                    help="folders of raw units (<x>/<unit>/jobs/<job>/config.json), task and agent from the unit name")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    rel = Path(a.release)
    task_dirs = {p.name: p for root in (rel / "tasks", rel / "open_ended" / "tasks") if root.is_dir()
                 for p in root.iterdir() if (p / "task.toml").exists()}
    cache, unexpected = {}, 0

    # 1. oracle and no-op validation runs: exact
    exact = sorted((rel / "validation").glob("*/*/config.json")) + sorted(
        (rel / "validation" / "rerun-20261110" / "runs").glob("*/jobs/*/config.json"))
    print("== oracle and no-op validation runs (must be identical)")
    for p in exact:
        rec = json.loads(p.read_text())
        task = next((t for t in task_dirs if t in str(p)), None)
        if task is None:
            rpath = (rec.get("tasks") or rec.get("datasets"))[0]["path"]
            task = Path(rpath).name
        agent = rec["agents"][0]["name"]
        ours = printed(rel, task_dirs[task], taskinfo.task_class(taskinfo.load(task_dirs[task])), agent, cache)
        same = normalize(rec) == normalize(ours)
        unexpected += not same
        print(f"  {'identical' if same else 'DIFFERENT'}  {agent:6s} {p.relative_to(rel)}")
        if not same:
            r, o = normalize(rec), normalize(ours)
            for k in sorted(set(r) | set(o)):
                if r.get(k) != o.get(k):
                    print(f"      {k}: recorded {json.dumps(r.get(k))}\n      {' ' * len(k)}  printed  {json.dumps(o.get(k))}")

    # 2. released model runs
    records = [(p, p.relative_to(rel).parts[-4], p.relative_to(rel).parts[-3])
               for p in sorted((rel / "runs").glob("*/*/a*/config.json"))
               + sorted((rel / "open_ended" / "runs").glob("*/*/a*/config.json"))]
    for x in a.extra_records:
        for p in sorted(Path(x).glob("*/jobs/*/config.json")):
            parts = p.relative_to(x).parts[0].split("__")  # <prefix>__<task>__<agent>__a<k>
            records.append((p, parts[1], parts[2]))
    stats = defaultdict(lambda: [0, 0, Counter(), []])
    for p, task, hint in records:
        rec = json.loads(p.read_text())
        agent = agent_key(rec, hint)
        cls = taskinfo.task_class(taskinfo.load(task_dirs[task]))
        ours = printed(rel, task_dirs[task], cls, agent, cache)
        kinds, bad = diff(normalize(rec), normalize(ours), task, agent)
        s = stats[(cls, agent)]
        s[0] += 1
        s[1] += not kinds and not bad
        s[2].update(kinds)
        if bad:
            s[3].append((p, bad))
    print("\n== released model runs: every difference explained?")
    print(f"  {'class':11s} {'agent':6s} {'runs':>5s} {'identical':>9s} {'unexpected':>10s}  explained differences (runs)")
    order = {"verifiable": 0, "broker": 1, "open-ended": 2}
    for (cls, agent), (n, same, kinds, bad) in sorted(stats.items(), key=lambda kv: (order[kv[0][0]], kv[0][1])):
        unexpected += len(bad)
        print(f"  {cls:11s} {agent:6s} {n:5d} {same:9d} {len(bad):10d}  "
              + ", ".join(f"{k} ({c})" for k, c in sorted(kinds.items())))
        for p, lines in bad[: (None if a.verbose else 3)]:
            print(f"      UNEXPECTED {p}")
            for line in lines:
                print(f"        {line}")
    print("\n  explained differences:")
    for k, v in WHY.items():
        print(f"    {k}: {v}")
    print(f"\n{'OK: nothing unexpected' if not unexpected else f'{unexpected} unexpected difference(s)'}")
    return 1 if unexpected else 0


if __name__ == "__main__":
    sys.exit(main())
