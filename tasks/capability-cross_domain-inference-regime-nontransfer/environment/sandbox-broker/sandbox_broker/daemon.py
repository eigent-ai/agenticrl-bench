"""Starting and supervising the gate daemon as root.

``start`` is meant to run once as root when the container comes up (for example from a
healthcheck). It moves the platform credentials from its environment into a root-only
file (then drops them from its own environment), checks that nothing the daemon will import
is writable by other users, launches a detached supervisor with a clean environment and
waits until the socket answers.
"""
from __future__ import annotations

import asyncio
import ctypes
import json
import logging
import os
import resource
import signal
import stat
import subprocess
import sys
import time
from typing import Any

from .config import (CONFIG_VAR, EXTRA_DOMAIN_VARS, PROVIDER_VAR, BackendConfig, ConfigError, credentials_from_env,
                     load_backend_config, provider_from_env, read_credentials, scrub_env, write_credentials)
from .policy import Policy, PolicyError, load_policy

log = logging.getLogger("sandbox_broker.daemon")

CLEAN_ENV = {"PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "LANG": "C.UTF-8",
             "HOME": "/root"}


def _child_env() -> dict:
    """CLEAN_ENV plus the non-secret run-time settings the daemon still needs (config.py)."""
    env = dict(CLEAN_ENV)
    for var in (*EXTRA_DOMAIN_VARS, CONFIG_VAR):
        if os.environ.get(var):
            env[var] = os.environ[var]
    return env


class StartError(RuntimeError):
    pass


def harden_process() -> None:
    """No core dumps and no ptrace/proc access from other users, even after a uid change."""
    try:
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    except (ValueError, OSError):
        pass
    try:
        libc = ctypes.CDLL(None, use_errno=True)
        libc.prctl(4, 0, 0, 0, 0)  # PR_SET_DUMPABLE = 4
    except (OSError, AttributeError):
        pass


# ---------------------------------------------------------------------------- config


def _backend_config(policy: Policy, path: str | None, *, strict: bool) -> BackendConfig:
    try:
        return load_backend_config(path, policy_path=policy.source_path, strict=strict,
                                   legacy=policy.legacy_backend)
    except (ConfigError, OSError, ValueError) as exc:
        raise StartError(f"backend config: {exc}") from exc


def _credentials_path(policy: Policy, cfg: BackendConfig) -> str:
    return cfg.credentials_file if cfg.credentials_source == "file" else policy.credentials_path


# ---------------------------------------------------------------------------- install checks


def _unsafe(path: str) -> str | None:
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        return None
    if stat.S_ISLNK(st.st_mode):
        return None
    reasons = []
    if st.st_uid != 0:
        reasons.append(f"owned by uid {st.st_uid}")
    if st.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
        reasons.append("writable by group/others")
    return f"{path} is {' and '.join(reasons)}" if reasons else None


def check_install_integrity(extra_paths: list[str] = ()) -> list[str]:
    """Everything the daemon imports must be writable only by root.

    Checks every directory on ``sys.path`` recursively, their parent directories, the
    interpreter and any extra paths (policy files).
    """
    problems: list[str] = []
    roots = [p for p in sys.path if p and os.path.isdir(p)]
    checked: set[str] = set()
    for root in roots + [os.path.dirname(os.path.realpath(sys.executable))]:
        parent = os.path.dirname(os.path.abspath(root))
        while parent not in checked:
            checked.add(parent)
            if (p := _unsafe(parent)):
                problems.append(p)
            if parent == os.path.dirname(parent):
                break
            parent = os.path.dirname(parent)
    for path in [os.path.realpath(sys.executable), *extra_paths]:
        if (p := _unsafe(path)):
            problems.append(p)
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            if dirpath in checked:
                continue
            checked.add(dirpath)
            if (p := _unsafe(dirpath)):
                problems.append(p)
            for name in filenames:
                if (p := _unsafe(os.path.join(dirpath, name))):
                    problems.append(p)
            if len(problems) > 20:
                return problems
    return problems


# ---------------------------------------------------------------------------- serve / supervise


def build_backend(policy: Policy, cfg: BackendConfig, *, strict: bool):
    """Instantiate the task's backend inside the root daemon (the only place SDKs load).

    The provider comes from the credentials record, where ``start`` put the task's choice
    (``cfg.provider`` is set only by the hidden ``--backend`` override).
    """
    from .backends import load_backend_class

    creds: dict = {}
    if cfg.credentials_source != "none":
        path = _credentials_path(policy, cfg)
        if os.path.exists(path):
            creds = read_credentials(path, strict=strict)
        elif cfg.provider != "local":
            raise StartError(f"no credentials at {path}")
    recorded = creds.pop("provider", None)
    cfg.provider = cfg.provider or recorded
    if not cfg.provider:
        creds.clear()
        raise StartError(f"no provider: the task sets {PROVIDER_VAR} (task.toml), which start records")
    try:
        cls = load_backend_class(cfg.provider)
        backend = cls.from_config(cfg.settings(), creds, state_dir=policy.state_dir)
    finally:
        parent = str(creds.get("parent_sandbox_id", ""))
        creds.clear()
    if policy.sandbox.network not in backend.network_modes:
        raise StartError(f"the configured backend cannot create sandboxes with network={policy.sandbox.network!r}")
    return backend, parent


def serve(policy_path: str | None, *, dev: bool = False, backend_name: str | None = None,
          backend_config: str | None = None) -> int:
    from .audit import AuditLog
    from .server import BrokerServer

    if not dev and os.geteuid() != 0:
        raise StartError("the gate daemon must run as root")
    os.umask(0o022)
    harden_process()
    policy = load_policy(policy_path, strict=not dev)
    cfg = _backend_config(policy, backend_config, strict=not dev)
    if backend_name:
        cfg.provider = backend_name
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    if policy.log_resolved_hosts:
        _log_resolved_hosts()
    backend, parent = build_backend(policy, cfg, strict=not dev)
    log.info("backend %s configured (backend config: %s)", cfg.provider, cfg.source_path or "legacy policy keys")
    audit = AuditLog(policy.audit_log, policy.audit_log_mode)
    server = BrokerServer(policy, backend, audit=audit, parent_id=parent)
    asyncio.run(server.serve())
    return 0


def _log_resolved_hosts() -> None:
    """Debug aid: log every hostname the daemon resolves (used to size network allowlists)."""
    import socket

    orig = socket.getaddrinfo
    seen: set[str] = set()

    def getaddrinfo(host, *args, **kwargs):
        if host not in seen:
            seen.add(host)
            log.info("resolving host %s", host)
        return orig(host, *args, **kwargs)

    socket.getaddrinfo = getaddrinfo


def _daemon_args(policy_path: str | None, backend_name: str | None, backend_config: str | None) -> list[str]:
    args = []
    if backend_name:
        args += ["--backend", backend_name]
    if policy_path:
        args += ["--config", policy_path]
    if backend_config:
        args += ["--backend-config", backend_config]
    return args


def supervise(policy_path: str | None, *, max_restarts: int = 20, backend_name: str | None = None,
              backend_config: str | None = None) -> int:
    harden_process()
    cmd = [sys.executable, "-I", "-m", "sandbox_broker", "serve", *_daemon_args(policy_path, backend_name, backend_config)]
    child: subprocess.Popen | None = None
    stopping = False

    def forward(sig, _frame):
        nonlocal stopping
        stopping = True
        if child and child.poll() is None:
            child.send_signal(sig)

    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        signal.signal(sig, forward)
    restarts = 0
    while True:
        started = time.monotonic()
        child = subprocess.Popen(cmd, env=_child_env(), cwd="/", close_fds=True)
        rc = child.wait()
        if stopping or rc == 0:
            return rc
        restarts = 0 if time.monotonic() - started > 300 else restarts + 1
        print(f"sandbox-gate: daemon exited with {rc}; restart {restarts}/{max_restarts}", file=sys.stderr, flush=True)
        if restarts >= max_restarts:
            return rc or 1
        time.sleep(min(30, 2 ** restarts))


# ---------------------------------------------------------------------------- start


def _ping(socket_path: str, timeout: float = 5.0) -> dict | None:
    from .client import BrokerClient

    try:
        return BrokerClient(socket_path, connect_timeout=timeout).ping(timeout=timeout)
    except Exception:  # noqa: BLE001
        return None


def _recorded_provider(path: str) -> str | None:
    try:
        return read_credentials(path, strict=True).get("provider")
    except (OSError, ValueError):
        return None


def capture_credentials(policy: Policy, cfg: BackendConfig, env: dict[str, str]) -> None:
    """Move the task's provider choice and env-provided credentials (plus the backend's runtime
    facts) into the root-only record."""
    from .backends import load_backend_class

    path = _credentials_path(policy, cfg)
    wanted = cfg.provider or provider_from_env(env)
    if cfg.credentials_source == "none":
        if not wanted:
            raise StartError(f"no provider: set {PROVIDER_VAR} (task.toml)")
        return
    if cfg.credentials_source == "file":
        if not os.path.exists(path):
            raise StartError(f"credentials file {path} does not exist")
        recorded = _recorded_provider(path)
        if not recorded and not cfg.provider:
            raise StartError(f"credentials file {path} names no provider")
        if wanted and recorded and wanted != recorded:
            raise StartError(f"the task asks for provider {wanted!r} but {path} holds {recorded!r} credentials")
        return
    creds = credentials_from_env(env)
    if creds:
        if not wanted:
            creds.clear()
            raise StartError(f"no provider: set {PROVIDER_VAR} (task.toml) next to the credentials")
        try:
            creds.update(load_backend_class(wanted).capture_runtime(env))
        except (ImportError, ValueError) as exc:
            creds.clear()
            raise StartError(f"backend {wanted!r} is not available: {exc}") from exc
        creds["provider"] = wanted
        write_credentials(path, creds)
        creds.clear()
        return
    if os.path.exists(path):  # a later start: the record from the first one stands
        recorded = _recorded_provider(path)
        if wanted and recorded and wanted != recorded:
            raise StartError(f"the task asks for provider {wanted!r} but the gate holds {recorded!r} credentials")
        return
    if wanted == "local":
        write_credentials(path, {"provider": wanted})
        return
    raise StartError("no credentials: the task maps host secrets to SANDBOX_GATE_TOKEN_ID/SECRET or "
                     "SANDBOX_GATE_CRED_* in task.toml (empty means the host variable was not set)")


def start(policy_path: str | None, *, wait_s: float = 120.0, backend_name: str | None = None,
          backend_config: str | None = None, check_install: bool = True) -> dict:
    """Idempotent: returns quickly when a healthy daemon is already serving."""
    if os.geteuid() != 0:
        raise StartError("start must run as root")
    try:
        policy: Policy = load_policy(policy_path, strict=True)
    except PolicyError as exc:
        raise StartError(str(exc)) from exc
    cfg = _backend_config(policy, backend_config, strict=True)
    if not backend_name and cfg.credentials_source == "none":
        backend_name = provider_from_env(os.environ)  # no record to carry it to the daemon
    if backend_name:
        cfg.provider = backend_name
    try:
        status = _ping(policy.socket_path)
        if status and status.get("ready") and status.get("euid") == 0:
            return status
        if check_install:
            extra = [p for p in (policy.source_path, cfg.source_path) if p]
            problems = check_install_integrity(extra)
            if problems:
                raise StartError("refusing to start; unsafe install:\n  " + "\n  ".join(problems[:20]))
        capture_credentials(policy, cfg, dict(os.environ))
    finally:
        scrub_env()  # credentials never outlive this step in any environment
    if status is None:
        os.makedirs(policy.log_dir, mode=0o755, exist_ok=True)
        logf = open(policy.daemon_log, "ab")
        os.chmod(policy.daemon_log, 0o640)
        cmd = [sys.executable, "-I", "-m", "sandbox_broker", "supervise",
               *_daemon_args(policy.source_path, backend_name, backend_config or cfg.source_path)]
        subprocess.Popen(cmd, env=_child_env(), cwd="/", stdin=subprocess.DEVNULL, stdout=logf,
                         stderr=subprocess.STDOUT, start_new_session=True, close_fds=True)
        logf.close()
    deadline = time.monotonic() + wait_s
    last = None
    while time.monotonic() < deadline:
        last = _ping(policy.socket_path)
        if last and last.get("ready"):
            return last
        time.sleep(0.5)
    tail = ""
    try:
        with open(policy.daemon_log, "rb") as f:
            f.seek(0, os.SEEK_END)
            f.seek(max(0, f.tell() - 4000))
            tail = f.read().decode("utf-8", "replace")
    except OSError:
        pass
    raise StartError(f"gate did not become ready within {wait_s:.0f}s; last status: {last}\n{tail}")
