"""One live rollout job of the terminal-agent RL setup on this box (run as root by srv/job.sh, for /opt/live/run.sh).

    agents (real Terminus-2 + 2 explorers per episode, LiteLLM; tmux sessions of their own task workspace)
        -> gateway in front of the proxy (the agents' traffic as it arrives; it sometimes drops a response after the
           proxy sent it, and an agent waiting on a slow answer may give up; agents retry)
        -> the proxy in /app/terminal_rl (run as the agent user, from its own tree)
        -> rollout gateway -> SGLang 0.5.9 serving Qwen3-4B-Instruct-2507 on the GPU
    trainer: pushes weights to the engine (update_weights_from_disk) while episodes run, so the engine aborts the
    generations in flight; at the end ``POST /s/<episode>/finish`` collects every episode's training rows.

Everything the job saw goes to --run-dir (meta.json, requests.jsonl.gz, engine.jsonl.gz, samples.json.gz,
clients.json, proxy.log). Exit 0: the job ran (whatever the proxy did); 3: the box itself failed (engine, tmux, ...).
"""
import argparse
import asyncio
import gzip
import json
import logging
import os
import shutil
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path, PurePosixPath

import aiohttp
from aiohttp import web

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gateway import Gateway  # noqa: E402
from treehash import tree_hash  # noqa: E402

JOB = "terminal-rl-live/1"
LIVE = Path("/opt/live")
TASKS = LIVE / "srv" / "tasks"
ENGINE_MODEL = str(LIVE / "models" / "Qwen3-4B-Instruct-2507")
PROXY_TREE = "/app/terminal_rl"
PROXY_USER = "agent"
PROXY_CMD = ["/usr/local/bin/python3", "-m", "terminal_rl.proxy"]
CONTEXT_LENGTH = 32768
PROXY_ARGS = ["--model-path", "/models/Qwen3-4B-Instruct-2507", "--reasoning-parser", "none",
              "--context-length", str(CONTEXT_LENGTH)]
# episode = (TMax task, Terminus-2 settings); workspace user ep<k>, home /home/ep<k>
EPISODES = [
    ("task_000171_03faa1d0", {"parser": "json"}),
    ("task_000659_f1cff69a", {"parser": "xml"}),
    ("task_000311_9e22fec5", {"parser": "json", "compact": True}),
    ("task_002440_8e14657f", {"parser": "json"}),
    ("task_003043_df5cd77b", {"parser": "xml"}),
    ("task_003767_c1ba81bd", {"parser": "json", "compact": True}),
    ("task_001360_2982e329", {"parser": "json"}),
    ("task_001344_00ae4249", {"parser": "json"}),
]
HELPERS = 2
MAIN_MAX_TURNS = 20
HELPER_MAX_TURNS = 6
MAX_TOKENS = 8192
JOB_DEADLINE_S = 2100
ENGINE_STALL_S = 300  # generations in flight, none finished for this long: the engine hangs (box-side failure)
GATEWAY_TIMEOUT_S = 1.0
EXPLORER_TASK = ("Another agent is about to work on the task below. Do not try to solve it. Use a few quick commands to "
                 "look around (relevant files, tools, versions, constraints), then reply with task_complete true and put "
                 "a short report of what you found in your analysis.\n\nTask:\n")

log = logging.getLogger("live")


class InfraError(RuntimeError):
    pass


def episode_id(k: int, task: str) -> str:
    return f"tmax-{task.split('_')[1]}-{k}"


def plan():
    """Episodes, conversations and the gateway's faults (fixed for this job version)."""
    eps, faults = [], {}
    for k, (task, cfg) in enumerate(EPISODES):
        eid = episode_id(k, task)
        convs = [eid] + [f"{eid}/explore-{j}" for j in range(HELPERS)]
        eps.append({"k": k, "id": eid, "task": task, "cfg": cfg, "user": f"ep{k}", "home": f"/home/ep{k}",
                    "conversations": convs})
        faults[eid] = {"lose": [0, 5], "timeout": [2]}
        for c in convs[1:]:
            faults[c] = {"lose": [0]}
    return eps, faults


def free_ports(n: int) -> list[int]:
    socks = []
    try:
        for _ in range(n):
            s = socket.socket()
            s.bind(("127.0.0.1", 0))
            socks.append(s)
        return [s.getsockname()[1] for s in socks]
    finally:
        for s in socks:
            s.close()


# ---------------------------------------------------------------------------------------------------------------------
class LocalEnv:
    """The episode's task workspace: commands run as the workspace user in its home, with its own tmux server."""

    default_user = None

    def __init__(self, user: str, home: str):
        self.user = user
        self.home = home
        self.session_id = user

    async def exec(self, command, cwd=None, env=None, timeout_sec=None, user=None, **kwargs):
        from harbor.environments.base import ExecResult

        e = {"HOME": self.home, "USER": self.user, "LOGNAME": self.user, "SHELL": "/bin/bash",
             "TERM": "xterm-256color", "LANG": "C.UTF-8", "PATH": "/usr/local/bin:/usr/bin:/bin",
             "TMUX_TMPDIR": f"{self.home}/.tmux"}
        for key, val in (env or {}).items():
            e[str(key)] = str(val)
        argv = ["runuser", "-u", self.user, "--", "env", "-i"] + [f"{k}={v}" for k, v in e.items()] + \
               ["bash", "-c", command]
        proc = await asyncio.create_subprocess_exec(*argv, cwd=cwd or self.home, stdin=subprocess.DEVNULL,
                                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                    start_new_session=True)
        try:
            out, err = await asyncio.wait_for(proc.communicate(), timeout=timeout_sec)
        except asyncio.TimeoutError:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except Exception:
                pass
            await proc.wait()
            return ExecResult(stdout="", stderr=f"timed out after {timeout_sec}s", return_code=124)
        return ExecResult(stdout=out.decode("utf-8", "replace"), stderr=err.decode("utf-8", "replace"),
                          return_code=proc.returncode)

    async def is_dir(self, path, **kwargs) -> bool:
        return False

    async def is_file(self, path, **kwargs) -> bool:
        return False

    async def upload_file(self, *args, **kwargs):
        raise NotImplementedError

    async def download_file(self, *args, **kwargs):
        raise NotImplementedError


def prepare_workspace(ep: dict) -> str:
    """Fresh home for the episode (the TMax task's files), as the task image would have it; returns the task text.
    The task's setup script runs as the workspace user (never as root: it writes to /tmp)."""
    user, home = ep["user"], ep["home"]
    subprocess.run(["pkill", "-KILL", "-u", user], check=False)
    time.sleep(0.2)
    shutil.rmtree(home, ignore_errors=True)
    os.makedirs(home, mode=0o700)
    shutil.chown(home, user, user)
    src = (TASKS / ep["task"] / "post_install.sh").read_text()
    lines = [ln for ln in src.splitlines()
             if not any(w in ln for w in ("apt-get ", "pip3 install", "pip install", "useradd "))]
    script = "\n".join(lines).replace("/home/user", home).replace("user:user", f"{user}:{user}") + "\n"
    script = f"set +e\numask 022\nmkdir -p {home}/.tmux {home}/.panes\n" + script + \
        f"chmod 0700 {home} {home}/.tmux {home}/.panes\n"
    r = subprocess.run(["runuser", "-u", user, "--", "env", "-i", f"HOME={home}", f"USER={user}", "LANG=C.UTF-8",
                        "PATH=/usr/local/bin:/usr/bin:/bin", "bash", "-c", script],
                       cwd=home, stdin=subprocess.DEVNULL, capture_output=True, timeout=300)
    if not (os.path.isdir(os.path.join(home, ".tmux")) and os.path.isdir(os.path.join(home, ".panes"))):
        raise InfraError(f"workspace setup of {ep['id']} failed: {r.stderr.decode()[-500:]}")
    return (TASKS / ep["task"] / "instruction.md").read_text().replace("/home/user", home)


# ---------------------------------------------------------------------------------------------------------------------
class Relay:
    """The gateway in front of the proxy: logs every request with its conversation, drops some finished responses
    (502 after the proxy answered) and gives up on some slow ones (504); a client never sees more than two failures in
    a row. Conversations whose first dropped response is still due are not touched by weight updates."""

    def __init__(self, proxy_url: str, faults: dict, timeout_s: float):
        self.proxy_url = proxy_url.rstrip("/")
        self.faults = faults
        self.timeout_s = timeout_s
        self.records: list[dict] = []
        self.count: dict[str, int] = {}
        self.state: dict[str, dict] = {}
        self.inflight: dict[str, int] = {}
        self.first_due = {c for c, f in faults.items() if f.get("lose")}
        self.updating = False
        self.idle = asyncio.Event()
        self.idle.set()
        self.http: aiohttp.ClientSession | None = None

    def protected_busy(self) -> bool:
        return any(self.inflight.get(c) for c in self.first_due)

    def total_inflight(self) -> int:
        return sum(self.inflight.values())

    async def handle(self, request: web.Request) -> web.Response:
        sid = request.match_info["sid"]
        raw = await request.read()
        try:
            body = json.loads(raw)
            assert isinstance(body, dict)
        except Exception:
            return web.json_response({"error": {"message": "bad request body", "code": 400}}, status=400)
        conv = request.headers.get("X-Session-ID") or body.get("session_id") or sid
        while conv in self.first_due and self.updating:
            await self.idle.wait()
        self.inflight[conv] = self.inflight.get(conv, 0) + 1
        try:
            return await self._handle(request, sid, conv, raw, body)
        finally:
            self.inflight[conv] -= 1

    async def _handle(self, request, sid, conv, raw, body) -> web.Response:
        n = self.count.get(conv, 0)
        self.count[conv] = n + 1
        rec = {"sid": sid, "conv": conv, "n": n, "t0": time.time(), "body": body}
        f = self.faults.get(conv, {})
        st = self.state.setdefault(conv, {"prev_failed": False, "lose": sorted(f.get("lose", [])),
                                          "timeout": sorted(f.get("timeout", [])), "first": bool(f.get("lose"))})
        do_timeout = bool(st["timeout"]) and n >= st["timeout"][0] and not st["prev_failed"]
        do_lose = not do_timeout and bool(st["lose"]) and n >= st["lose"][0] and not st["prev_failed"]
        if self.http is None:
            self.http = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=900),
                                              connector=aiohttp.TCPConnector(limit=0))
        headers = {"Content-Type": "application/json"}
        if request.headers.get("X-Session-ID"):
            headers["X-Session-ID"] = request.headers["X-Session-ID"]

        async def call():
            async with self.http.post(f"{self.proxy_url}/s/{sid}/v1/chat/completions", data=raw, headers=headers) as r:
                return r.status, await r.text()

        timed_out = False
        try:
            if do_timeout:
                st["timeout"].pop(0)
                try:
                    status, text = await asyncio.wait_for(call(), timeout=self.timeout_s)
                except asyncio.TimeoutError:
                    timed_out, status, text = True, 504, ""
            else:
                status, text = await call()
        except Exception as e:
            status, text = 599, f"proxy unreachable: {e}"
        rec.update(t1=time.time(), status=status, timed_out=timed_out)
        if status == 200:
            try:
                rec["response"] = json.loads(text)
            except json.JSONDecodeError:
                rec["status"] = status = 598
        elif not timed_out:
            rec["error"] = text[:2000]
        lost = do_lose and status == 200
        if lost:
            st["lose"].pop(0)
            if st["first"]:
                st["first"] = False
                self.first_due.discard(conv)
        st["prev_failed"] = status != 200 or lost
        rec["lost"] = lost
        rec["delivered"] = status == 200 and not lost
        self.records.append(rec)
        if timed_out:
            return web.json_response({"error": {"message": "gateway timeout", "type": "Timeout", "code": 504}},
                                     status=504)
        if lost:
            return web.json_response({"error": {"message": "upstream connection reset", "type": "InternalServerError",
                                                "code": 502}}, status=502)
        return web.Response(text=text, status=status, content_type="application/json")

    def app(self) -> web.Application:
        app = web.Application(client_max_size=256 * 1024 * 1024)
        app.router.add_post("/s/{sid}/v1/chat/completions", self.handle)
        return app

    async def close(self):
        if self.http is not None:
            await self.http.close()


class Trainer:
    """Pushes weights to the engine while the episodes run (same checkpoint; SGLang aborts what is in flight)."""

    def __init__(self, gw: Gateway, relay: Relay, updates: int = 4, max_attempts: int = 8, first_after: float = 30.0,
                 every: float = 45.0):
        self.gw, self.relay = gw, relay
        self.updates, self.max_attempts = updates, max_attempts
        self.first_after, self.every = first_after, every
        self.hits = 0

    def _generating(self) -> bool:
        now = time.time()
        return any(now - st["t0"] >= 0.5 for st in self.gw.inflight.values())

    async def _window(self, timeout: float) -> bool:
        t_end = time.time() + timeout
        while time.time() < t_end:
            if self._generating():
                self.relay.updating = True
                self.relay.idle.clear()
                if not self.relay.protected_busy():
                    return True
                self.relay.updating = False
                self.relay.idle.set()
            await asyncio.sleep(0.2)
        return False

    async def run(self):
        await asyncio.sleep(self.first_after)
        attempts = 0
        while attempts < self.max_attempts and (self.hits < 1 or attempts < self.updates):
            if not await self._window(120.0):
                continue
            attempts += 1
            u = {"id": attempts, "u0": time.time()}
            self.gw.updates.append(u)
            try:
                status, text = await self.gw.engine_post(
                    "/update_weights_from_disk", {"model_path": ENGINE_MODEL, "abort_all_requests": True,
                                                  "weight_version": f"live-{attempts}"}, timeout=900)
                u.update(status=status, message=text[:300])
            except Exception as e:
                u.update(status=0, message=f"{type(e).__name__}: {e}"[:300])
            finally:
                u["u1"] = time.time()
                self.relay.updating = False
                self.relay.idle.set()
            await asyncio.sleep(2.0)
            u["aborted"] = sum(1 for c in self.gw.log if c["ended"] == "injected_abort" and c["t0"] <= u["u0"] <= c["t1"])
            self.hits += u["aborted"] > 0
            log.info("weight update %d: %s, %d generations aborted", attempts, u.get("status"), u["aborted"])
            await asyncio.sleep(self.every)


# ---------------------------------------------------------------------------------------------------------------------
def _terminus(logs_dir: Path, base: str, sid: str, cfg: dict, helper: bool):
    from harbor.agents.terminus_2 import Terminus2

    # the agents' own context budget leaves room for a full max_tokens answer within the proxy's context length
    ctx = 12000 if cfg.get("compact") else CONTEXT_LENGTH - MAX_TOKENS
    return Terminus2(
        logs_dir=logs_dir, model_name="hosted_vllm/policy", api_base=base, session_id=sid, temperature=1.0,
        parser_name="json" if helper else cfg.get("parser", "json"), interleaved_thinking=False,
        enable_summarize=not helper, proactive_summarization_threshold=4000 if cfg.get("compact") else 8000,
        model_info={"max_input_tokens": ctx, "max_output_tokens": 8192, "input_cost_per_token": 0.0,
                    "output_cost_per_token": 0.0},
        llm_call_kwargs={"max_tokens": MAX_TOKENS}, record_terminal_session=False, suppress_max_turns_warning=True,
        max_turns=HELPER_MAX_TURNS if helper else MAIN_MAX_TURNS)


async def _run_agent(agent, instruction: str, env) -> tuple[str | None, str]:
    from harbor.models.agent.context import AgentContext

    err = None
    try:
        await agent.run(instruction, environment=env, context=AgentContext())
    except Exception as e:
        err = f"{type(e).__name__}: {e}"
    report = ""
    for m in reversed(agent._chat.messages if agent._chat else []):
        if m.get("role") == "assistant":
            report = m.get("content") or ""
            break
    return err, report[-1500:]


async def run_episode(ep: dict, sessions: dict, instruction: str, relay_url: str, run_dir: Path, results: list):
    base = f"{relay_url}/s/{ep['id']}/v1"
    env = LocalEnv(ep["user"], ep["home"])
    t0 = time.time()

    async def helper(j: int) -> str:
        sid = f"{ep['id']}/explore-{j}"
        agent = _terminus(run_dir / "agents" / sid.replace("/", "_"), base, sid, ep["cfg"], helper=True)
        agent._session = sessions[sid]
        err, rep = await _run_agent(agent, EXPLORER_TASK + instruction, env)
        results.append({"sid": sid, "error": err, "episodes": agent._n_episodes, "helper": True})
        return rep

    reps = await asyncio.gather(*[helper(j) for j in range(HELPERS)])
    task = instruction + "\n\nNotes from helper agents that already looked around:\n" + "\n\n".join(
        f"[helper {j}] {r}" for j, r in enumerate(reps))
    agent = _terminus(run_dir / "agents" / ep["id"], base, ep["id"], ep["cfg"], helper=False)
    agent._session = sessions[ep["id"]]
    err, _ = await _run_agent(agent, task, env)
    results.append({"sid": ep["id"], "error": err, "seconds": round(time.time() - t0, 1),
                    "episodes": agent._n_episodes, "summarizations": agent._summarization_count})


async def start_sessions(ep: dict) -> dict:
    from harbor.agents.terminus_2.tmux_session import TmuxSession

    env = LocalEnv(ep["user"], ep["home"])
    out = {}
    for sid in ep["conversations"]:
        name = "main" if sid == ep["id"] else sid.rsplit("/", 1)[1]
        # each agent's shell prompt carries the name of its tmux session
        sess = TmuxSession(session_name=name, environment=env,
                           logging_path=PurePosixPath(f"{ep['home']}/.panes/{name}.pane"),
                           local_asciinema_recording_path=None, remote_asciinema_recording_path=None, user=None,
                           extra_env={"debian_chroot": name})
        try:
            await sess.start()
        except Exception as e:
            raise InfraError(f"tmux session {sid}: {e}")
        out[sid] = sess
    return out


# ---------------------------------------------------------------------------------------------------------------------
def start_proxy(port: int, engine_url: str, logf):
    argv = ["runuser", "-u", PROXY_USER, "--", "env", f"HOME=/home/{PROXY_USER}"] + PROXY_CMD + \
           ["--engine-url", engine_url, "--host", "127.0.0.1", "--port", str(port)] + PROXY_ARGS
    env = {k: v for k, v in os.environ.items() if not any(s in k for s in ("TOKEN", "SECRET", "KEY", "PASSWORD"))}
    env.update(PYTHONUNBUFFERED="1", HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1")
    return subprocess.Popen(argv, cwd=PROXY_TREE, env=env, stdout=logf, stderr=subprocess.STDOUT,
                            start_new_session=True)


def stop_proxy(p):
    for sig, wait in ((signal.SIGTERM, 10), (signal.SIGKILL, 5)):
        try:
            os.killpg(p.pid, sig)
            p.wait(timeout=wait)
            return
        except Exception:
            pass


async def wait_http(url: str, timeout: float, proc=None) -> bool:
    t_end = time.time() + timeout
    async with aiohttp.ClientSession() as http:
        while time.time() < t_end:
            if proc is not None and proc.poll() is not None:
                return False
            try:
                async with http.get(url, timeout=aiohttp.ClientTimeout(total=5)) as r:
                    if r.status == 200:
                        return True
            except Exception:
                pass
            await asyncio.sleep(0.5)
    return False


async def start_site(app: web.Application, port: int) -> web.AppRunner:
    runner = web.AppRunner(app, access_log=None)
    await runner.setup()
    await web.TCPSite(runner, "127.0.0.1", port).start()
    return runner


def _dump_jsonl_gz(path: Path, rows):
    with gzip.open(path, "wt") as f:
        for r in rows:
            f.write(json.dumps({k: v for k, v in r.items() if not k.startswith("_")}) + "\n")


async def amain(run_dir: Path) -> int:
    eps, faults = plan()
    meta = {"job": JOB, "run_id": run_dir.name, "t_start": time.time(), "status": "starting",
            "episodes": [{k: e[k] for k in ("id", "task", "cfg", "conversations")} for e in eps], "faults": faults,
            "coverage_faults": {c: {"lose": [0]} for e in eps for c in e["conversations"]},
            "proxy_cmd": PROXY_CMD, "proxy_args": PROXY_ARGS, "context_length": CONTEXT_LENGTH,
            "gateway_timeout_s": GATEWAY_TIMEOUT_S, "max_tokens": MAX_TOKENS}
    gw = Gateway(record=True)
    probe = await wait_http(gw.engine_url + "/health", 30)
    if not probe:
        raise InfraError("the engine is not up")

    (run_dir / "agents").mkdir(exist_ok=True)
    instructions, sessions = {}, {}
    for ep in eps:
        instructions[ep["id"]] = prepare_workspace(ep)
    for ep in eps:
        sessions.update(await start_sessions(ep))

    g_port, r_port, p_port = free_ports(3)
    g_runner = await start_site(gw.app(), g_port)
    relay = Relay(f"http://127.0.0.1:{p_port}", faults, GATEWAY_TIMEOUT_S)
    r_runner = await start_site(relay.app(), r_port)
    meta["tree_sha256_start"] = tree_hash(PROXY_TREE)
    logf = open(run_dir / "proxy.log", "w")
    proxy, results, samples, trainer_task = None, [], {}, None
    try:
        for attempt in range(2):  # a start-up failure such as a port taken meanwhile is retried once
            proxy = start_proxy(p_port, f"http://127.0.0.1:{g_port}", logf)
            if await wait_http(f"http://127.0.0.1:{p_port}/health", 180, proc=proxy):
                break
            stop_proxy(proxy)
            p_port = free_ports(1)[0]
            relay.proxy_url = f"http://127.0.0.1:{p_port}"
        else:
            meta["status"] = "proxy_unhealthy"
            print("[live] the proxy did not answer /health within 180 s (see the proxy log)", flush=True)
            return 0
        print(f"[live] proxy up; {len(eps)} episodes x {1 + HELPERS} agents starting", flush=True)
        trainer = Trainer(gw, relay)
        trainer_task = asyncio.ensure_future(trainer.run())
        relay_url = f"http://127.0.0.1:{r_port}"
        jobs = [asyncio.ensure_future(run_episode(ep, sessions, instructions[ep["id"]], relay_url, run_dir, results))
                for ep in eps]
        t_end = time.time() + JOB_DEADLINE_S
        pending, stalled = set(jobs), False
        while pending and time.time() < t_end and not stalled:
            _, pending = await asyncio.wait(pending, timeout=10)
            now = time.time()
            last = max([c["t1"] for c in gw.log[-1:]] + [meta["t_start"]])
            stalled = any(now - st["t0"] > ENGINE_STALL_S for st in gw.inflight.values()) and now - last > ENGINE_STALL_S
        done = [j for j in jobs if j.done()]
        meta["status"] = "completed" if not pending else ("engine_stalled" if stalled else "deadline")
        for j in pending:
            j.cancel()
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
        if stalled:
            (run_dir / "engine_stalled").touch()
            raise InfraError(f"the engine stopped making progress for {ENGINE_STALL_S} s with generations in flight")
        for j in done:
            if j.exception() is not None:
                raise j.exception()
        trainer_task.cancel()
        await asyncio.gather(trainer_task, return_exceptions=True)
        t_drain = time.time() + 120
        while (relay.total_inflight() or gw.inflight) and time.time() < t_drain:
            await asyncio.sleep(0.5)
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=300)) as http:
            for ep in eps:
                try:
                    async with http.post(f"http://127.0.0.1:{p_port}/s/{ep['id']}/finish", json={}) as resp:
                        samples[ep["id"]] = (await resp.json()).get("samples") if resp.status == 200 else None
                except Exception as e:
                    log.warning("finish %s failed: %s", ep["id"], e)
                    samples[ep["id"]] = None
    finally:
        if trainer_task is not None and not trainer_task.done():
            trainer_task.cancel()
        relay.updating = False
        relay.idle.set()
        if proxy is not None:
            stop_proxy(proxy)
        logf.close()
        for ep in eps:
            subprocess.run(["pkill", "-KILL", "-u", ep["user"]], check=False)
        await relay.close()
        await r_runner.cleanup()
        await g_runner.cleanup()
        healthy = await wait_http(gw.engine_url + "/health", 60)
        await gw.close()
        meta["t_end"] = time.time()
        meta["tree_sha256_end"] = tree_hash(PROXY_TREE)
        meta["updates"] = gw.updates
        meta["engine_healthy_at_end"] = healthy
        meta["engine_unreachable"] = gw.failures
        _dump_jsonl_gz(run_dir / "requests.jsonl.gz", relay.records)
        _dump_jsonl_gz(run_dir / "engine.jsonl.gz", gw.log)
        _dump_jsonl_gz(run_dir / "refused.jsonl.gz", gw.refused)
        with gzip.open(run_dir / "samples.json.gz", "wt") as f:
            json.dump(samples, f)
        json.dump(results, open(run_dir / "clients.json", "w"), indent=1)
        json.dump(meta, open(run_dir / "meta.json", "w"), indent=1)
        summarize(meta, eps, relay, gw, results, samples)
    if not healthy:
        raise InfraError("the engine went down during the job")
    if gw.failures:
        raise InfraError(f"the gateway could not reach the engine {len(gw.failures)} time(s): {gw.failures[0]['error']}")
    return 0


def summarize(meta, eps, relay, gw, results, samples):
    recs = relay.records
    n_rows = sum(len(s) for s in samples.values() if isinstance(s, list))
    upd = [u for u in meta.get("updates", []) if u.get("status") == 200]
    print(f"[live] run {meta['run_id']} ({meta['status']}): {len(recs)} agent requests "
          f"({sum(r['status'] == 200 for r in recs)} answered 200), {sum(bool(r.get('lost')) for r in recs)} responses "
          f"dropped after the proxy sent them, {sum(bool(r.get('timed_out')) for r in recs)} given up by the gateway, "
          f"{len(gw.log)} engine generations, {len(upd)} weight updates "
          f"({sum(c['ended'] == 'injected_abort' for c in gw.log)} generations aborted by them), "
          f"{n_rows} rows from finish", flush=True)
    errs = {r["sid"]: r.get("error") for r in results}
    for ep in eps:
        n = sum(1 for r in recs if r["sid"] == ep["id"])
        s = samples.get(ep["id"])
        rows = len(s) if isinstance(s, list) else "no samples (finish failed)"
        print(f"[live]   {ep['id']}: {n} requests, rows: {rows}", flush=True)
        for c in ep["conversations"]:
            if errs.get(c):
                print(f"[live]     {c}: {str(errs[c])[:300]}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    args = ap.parse_args()
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    log.setLevel(logging.INFO)
    os.environ.setdefault("LITELLM_LOCAL_MODEL_COST_MAP", "True")
    os.environ.setdefault("OPENAI_API_KEY", "sk-local-proxy")
    import harbor.utils.logger  # noqa: F401
    import importlib
    import litellm  # noqa: F401
    for mod in ("litellm.utils", "litellm.main", "litellm.rust_bridge.catalog", "litellm.rust_bridge.logger",
                "litellm.rust_bridge.tokenizer", "litellm.rust_bridge.configuration", "harbor.agents.terminus_2",
                "harbor.agents.terminus_2.tmux_session", "harbor.llms.lite_llm"):
        try:
            importlib.import_module(mod)
        except ImportError:
            pass
    for name in list(logging.root.manager.loggerDict):
        if name.startswith(("harbor", "LiteLLM", "litellm", "httpx")):
            logging.getLogger(name).setLevel(logging.CRITICAL)
    run_dir = Path(args.run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    try:
        rc = asyncio.run(amain(run_dir))
    except InfraError as e:
        print(f"[live] the box failed, not the proxy: {e}", flush=True)
        rc = 3
    except Exception as e:
        logging.exception("job crashed")
        print(f"[live] the job itself crashed: {type(e).__name__}: {e}", flush=True)
        rc = 3
    sys.exit(rc)


if __name__ == "__main__":
    main()
