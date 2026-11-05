"""Harbor backend: CPU sandboxes on any platform Harbor supports, through Harbor's own environment classes.

Chosen at launch, with no image or task.toml change: ``SANDBOX_GATE_PROVIDER=harbor`` plus
``SANDBOX_GATE_CRED_HARBOR_ENV_TYPE=<type>`` (a Harbor environment type: e2b, runloop, daytona, modal, ...) and the
platform's own credential variables as ``SANDBOX_GATE_CRED_<NAME>`` (``SANDBOX_GATE_CRED_E2B_API_KEY`` for
``E2B_API_KEY``). ``start`` captures them into the root-only record like any other credential; this backend puts
each field back under its native (upper-case) name into the root daemon's own environment, where the platform SDKs
look for it, and nowhere else. ``SANDBOX_GATE_TOKEN_ID/SECRET`` and ``SANDBOX_GATE_PROVIDER_ENV`` count only for
type modal (``MODAL_TOKEN_ID/SECRET``, ``MODAL_ENVIRONMENT``). Optional ``SANDBOX_GATE_CRED_HARBOR_KWARGS``: a JSON
object of extra keyword arguments for the Harbor environment class (e.g. a platform TTL), merged over
``[harbor] kwargs``.

Root-only backend config table, all keys optional::

    [harbor]
    env_type = "e2b"                          # when SANDBOX_GATE_CRED_HARBOR_ENV_TYPE is not set
    kwargs = {}                               # extra keyword arguments for the Harbor environment class
    venv = "/opt/sandbox-broker/harbor-venv"  # where the image installed the "harbor" extra

Harbor and its platform SDKs live in their own root-only venv, not in the daemon's, so the packages of the other
backends keep their versions. The daemon puts that venv first on its import path only when this backend starts,
after checking that everything in it is owned by root and not writable by others.

Contract notes:

* network: ``"none"`` is Harbor's ``no-network``, ``"egress"`` its ``public``. Harbor refuses, when the environment
  is constructed, a platform that cannot enforce the policy, so ``create`` raises for it.
* cpu / memory: Harbor takes whole cores, so cpu is rounded up; memory in MiB as given.
* lifetime: Harbor has no generic lifetime or idle setting; the gate's reaper terminates at the deadline, and
  platform TTLs can be set through ``kwargs``.
* images: a registry image is Harbor's ``docker_image``; a build context is the environment directory; setup
  commands become ``RUN`` lines of a derived Dockerfile. Platforms that start only from a prebuilt image (prime,
  opensandbox, cwsandbox, smol, hf-sandbox) take neither a build context nor setup commands (ImageBuildError).
* exec: argv is quoted into one POSIX command line, run as the platform's default user. Harbor returns text, so
  bytes that are not UTF-8 arrive replaced. stdin is uploaded to a temporary file and redirected (no stdin means
  /dev/null). Output is streamed where the Harbor environment streams, else sent in one piece at the end. A timeout
  counts as one whether Harbor raises or returns 124.
* files: through a temporary file (binary-safe), then chmod.
* poll: ``true`` in the sandbox; three failed polls in a row count as exited.
* attach: impossible (a Harbor environment cannot be re-acquired after a daemon restart); such sandboxes are
  reported lost and end with the platform's own TTL.
* hostname: no native option; the gate's fallback applies when the policy sets one.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import math
import os
import posixpath
import re
import shlex
import shutil
import site
import stat
import sys
import tempfile
import time
import types
import uuid
from pathlib import Path
from typing import Any, Mapping

from .base import (NETWORK_EGRESS, NETWORK_NONE, Backend, CreateSpec, ExecOutcome, FileTooLarge, ImageBuildError,
                   ImageSpec, OutputCallback)

log = logging.getLogger("sandbox_broker.harbor")

DEFAULT_VENV = "/opt/sandbox-broker/harbor-venv"
SETTINGS = {"env_type", "kwargs", "venv"}
#: Harbor platforms that start only from a prebuilt image
IMAGE_ONLY = {"prime", "opensandbox", "cwsandbox", "smol", "hf-sandbox"}
#: constructor arguments this backend sets itself
RESERVED_KWARGS = {"environment_dir", "environment_name", "session_id", "trial_paths", "task_env_config", "logger",
                   "persistent_env", "mounts", "network_policy", "phase_network_policies", "override_cpus",
                   "override_memory_mb", "override_gpus", "override_tpu", "extra_docker_compose"}
#: credential fields that are not platform variables
OWN_FIELDS = {"harbor_env_type", "harbor_kwargs", "token_id", "token_secret", "environment", "provider",
              "parent_sandbox_id"}
_ENV_NAME = re.compile(r"[A-Z_][A-Z0-9_]*")
_PROTECTED = {"PATH", "HOME", "SHELL", "USER", "LOGNAME", "PWD", "LANG", "TMPDIR"}
_PROTECTED_PREFIXES = ("LD_", "PYTHON", "SANDBOX_GATE_", "SANDBOX_BROKER_")
STDIN_DIR = "/tmp/.sandbox-gate-stdin"
EXEC_GRACE_S = 30
TIMEOUT_RC = 124
POLL_FAILURES = 3


def native_credentials(env_type: str, credentials: Mapping[str, Any]) -> dict[str, str]:
    """The daemon environment variables for the platform SDK, from the credentials record."""
    out: dict[str, str] = {}
    for field, value in credentials.items():
        if field in OWN_FIELDS or value in (None, ""):
            continue
        name = str(field).upper()
        if not _ENV_NAME.fullmatch(name) or name in _PROTECTED or name.startswith(_PROTECTED_PREFIXES):
            raise ValueError(f"credential field {field!r} cannot become a daemon environment variable")
        out[name] = str(value)
    if env_type == "modal":
        if credentials.get("token_id") and credentials.get("token_secret"):
            out.setdefault("MODAL_TOKEN_ID", str(credentials["token_id"]))
            out.setdefault("MODAL_TOKEN_SECRET", str(credentials["token_secret"]))
        if credentials.get("environment"):
            out.setdefault("MODAL_ENVIRONMENT", str(credentials["environment"]))
    return out


def unsafe_paths(root: str, limit: int = 20) -> list[str]:
    """Everything under ``root`` (and its parent directories) must be owned by root and not group/other-writable."""
    problems: list[str] = []

    def check(path: str) -> None:
        try:
            st = os.lstat(path)
        except FileNotFoundError:
            return
        if stat.S_ISLNK(st.st_mode):
            return
        reasons = []
        if st.st_uid != 0:
            reasons.append(f"owned by uid {st.st_uid}")
        if st.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
            reasons.append("writable by group/others")
        if reasons:
            problems.append(f"{path} is {' and '.join(reasons)}")

    parent = os.path.dirname(os.path.abspath(root))
    while True:
        check(parent)
        if parent == os.path.dirname(parent):
            break
        parent = os.path.dirname(parent)
    for dirpath, _dirnames, filenames in os.walk(root):
        check(dirpath)
        for name in filenames:
            check(os.path.join(dirpath, name))
        if len(problems) >= limit:
            break
    return problems[:limit]


def use_venv(venv: str) -> None:
    """Put the venv's site-packages (and what its .pth files add) first on this process's import path."""
    lib = os.path.join(venv, "lib", f"python{sys.version_info[0]}.{sys.version_info[1]}", "site-packages")
    if lib in sys.path:
        return
    if not os.path.isdir(lib):
        raise RuntimeError(f"the harbor backend needs Harbor installed in {venv} for this Python "
                           f"({sys.version_info[0]}.{sys.version_info[1]}); the image has no such venv")
    strict = os.geteuid() == 0
    if strict and (problems := unsafe_paths(venv)):
        raise RuntimeError("refusing to load the harbor venv; unsafe install:\n  " + "\n  ".join(problems))
    before = list(sys.path)
    site.addsitedir(lib)
    added = [p for p in sys.path if p not in before]
    if strict:
        for path in added:
            if not os.path.abspath(path).startswith(os.path.abspath(venv) + os.sep):
                if problems := unsafe_paths(path):
                    sys.path[:] = before
                    raise RuntimeError("refusing to load the harbor venv; unsafe path:\n  " + "\n  ".join(problems))
    sys.path[:] = added + before


def build_command(argv: list[str], stdin_path: str | None) -> str:
    """One POSIX shell command line that runs ``argv`` without further shell interpretation."""
    if not argv:
        raise ValueError("empty argv")
    return f"{shlex.join(argv)} < {shlex.quote(stdin_path) if stdin_path else '/dev/null'}"


def _class_names(exc: BaseException) -> list[str]:
    return [t.__name__ for t in type(exc).__mro__]


def _is_build_failure(exc: BaseException) -> bool:
    if any("BuildFailed" in n or "ImageBuild" in n for n in _class_names(exc)):
        return True
    text = str(exc).lower()
    return "build failed" in text or "build_failed" in text or "failed to build" in text


def _is_timeout(exc: BaseException) -> bool:
    return any("Timeout" in n for n in _class_names(exc))


class HarborBackend(Backend):
    name = "harbor"
    native_hostname = False
    network_modes = (NETWORK_NONE, NETWORK_EGRESS)

    @classmethod
    def from_config(cls, settings: Mapping[str, Any], credentials: Mapping[str, Any], *,
                    state_dir: str) -> "HarborBackend":
        provider = dict(settings.get("settings") or {})
        unknown = set(provider) - SETTINGS
        if unknown:
            raise ValueError(f"unknown [harbor] key(s): {', '.join(sorted(unknown))}")
        net = dict(settings.get("parent_network") or {})
        net.pop("extra_domains", None)
        if net:
            raise ValueError("the harbor backend does not manage this container's allowlist; "
                             "remove [harbor.parent_network]")
        env_type = str(credentials.get("harbor_env_type") or provider.get("env_type") or "").strip().lower()
        if not env_type:
            raise ValueError("harbor backend needs a Harbor environment type (SANDBOX_GATE_CRED_HARBOR_ENV_TYPE)")
        kwargs = dict(provider.get("kwargs") or {})
        if credentials.get("harbor_kwargs"):
            try:
                extra = json.loads(credentials["harbor_kwargs"])
            except ValueError:
                raise ValueError("SANDBOX_GATE_CRED_HARBOR_KWARGS is not valid JSON") from None
            if not isinstance(extra, dict):
                raise ValueError("SANDBOX_GATE_CRED_HARBOR_KWARGS must be a JSON object")
            kwargs.update(extra)
        reserved = set(kwargs) & RESERVED_KWARGS
        if reserved:
            raise ValueError(f"harbor kwargs cannot set {', '.join(sorted(reserved))}")
        return cls(env_type, state_dir=state_dir, kwargs=kwargs, env=native_credentials(env_type, credentials),
                   venv=str(provider.get("venv") or DEFAULT_VENV))

    def __init__(self, env_type: str, *, state_dir: str, kwargs: dict[str, Any] | None = None,
                 env: dict[str, str] | None = None, venv: str = DEFAULT_VENV):
        self.env_type = env_type
        self.kwargs = dict(kwargs or {})
        self.venv = venv
        self._env_vars = dict(env or {})
        self._root = os.path.join(state_dir, "harbor")
        self._h: types.SimpleNamespace | None = None
        self._envs: dict[str, Any] = {}
        self._workdirs: dict[str, str] = {}
        self._trials: dict[str, str] = {}
        self._poll_failures: dict[str, int] = {}
        self._background: set[asyncio.Task] = set()

    # ------------------------------------------------------------------ lifecycle

    async def start(self) -> None:
        if self._h is None:
            await asyncio.to_thread(self._load_harbor)

    def _load_harbor(self) -> None:
        use_venv(self.venv)
        os.environ.setdefault("LITELLM_LOCAL_MODEL_COST_MAP", "True")  # no model-cost download at import
        if self._env_vars:
            os.environ.update(self._env_vars)  # this root daemon's own environment only
            self._env_vars = {}
        from harbor.environments.factory import EnvironmentFactory
        from harbor.models.environment_type import EnvironmentType
        from harbor.models.task.config import EnvironmentConfig, NetworkMode, NetworkPolicy
        from harbor.models.trial.paths import TrialPaths

        try:
            env_type = EnvironmentType(self.env_type)
        except ValueError:
            raise ValueError(f"unknown Harbor environment type {self.env_type!r}; "
                             f"known: {', '.join(t.value for t in EnvironmentType)}") from None
        try:
            EnvironmentFactory.run_preflight(env_type)
        except SystemExit as exc:  # Harbor's preflight exits on missing credentials
            raise RuntimeError(f"Harbor preflight for {self.env_type} failed: {exc}") from None
        for sub in ("trials", "contexts", "tmp"):
            os.makedirs(os.path.join(self._root, sub), mode=0o700, exist_ok=True)
        self._h = types.SimpleNamespace(EnvironmentFactory=EnvironmentFactory, type=env_type,
                                        EnvironmentConfig=EnvironmentConfig, NetworkMode=NetworkMode,
                                        NetworkPolicy=NetworkPolicy, TrialPaths=TrialPaths)
        log.info("harbor backend ready: environment type %s", self.env_type)

    async def close(self) -> None:
        leftover = list(self._envs)
        await asyncio.gather(*(self.terminate(sid) for sid in leftover), return_exceptions=True)
        if self._background:
            await asyncio.gather(*self._background, return_exceptions=True)

    # ------------------------------------------------------------------ images

    def _definition(self, image: ImageSpec) -> tuple[str, str | None, str]:
        """(environment dir, docker_image, environment name) for Harbor."""
        key = hashlib.sha256(json.dumps([image.kind, image.pull_ref, image.context_sha256,
                                         list(image.setup_commands)]).encode()).hexdigest()
        name = f"sandbox-gate-{key[:12]}"
        if image.kind not in ("registry", "context"):
            raise ValueError(f"unknown image kind {image.kind}")
        if image.kind == "registry" and not image.setup_commands:
            empty = os.path.join(self._root, "empty")
            os.makedirs(empty, mode=0o700, exist_ok=True)
            return empty, image.pull_ref, name
        if self.env_type in IMAGE_ONLY:
            raise ImageBuildError(f"Harbor's {self.env_type} environment starts only from a prebuilt image; "
                                  "it cannot build a context or run setup commands")
        if image.kind == "context" and not image.setup_commands:
            return image.context_dir, None, name
        for cmd in image.setup_commands:
            if "\n" in cmd or "\r" in cmd:
                raise ImageBuildError("setup commands must be single lines for the harbor backend")
        derived = os.path.join(self._root, "contexts", key)
        if not os.path.isdir(derived):
            tmp = tempfile.mkdtemp(prefix=".incoming-", dir=os.path.join(self._root, "contexts"))
            try:
                if image.kind == "registry":
                    head = f"FROM {image.pull_ref}"
                else:
                    shutil.copytree(image.context_dir, tmp, symlinks=True, dirs_exist_ok=True)
                    head = Path(tmp, "Dockerfile").read_text().rstrip("\n")
                lines = [head, *(f"RUN {cmd}" for cmd in image.setup_commands)]
                Path(tmp, "Dockerfile").write_text("\n".join(lines) + "\n")
                try:
                    os.rename(tmp, derived)
                except OSError:
                    if not os.path.isdir(derived):
                        raise
                    shutil.rmtree(tmp, ignore_errors=True)  # a concurrent create got there first
            except BaseException:
                shutil.rmtree(tmp, ignore_errors=True)
                raise
        return derived, None, name

    # ------------------------------------------------------------------ sandboxes

    async def create(self, spec: CreateSpec) -> str:
        h = self._h
        if spec.network not in (NETWORK_NONE, NETWORK_EGRESS):
            raise ValueError(f"unsupported network mode {spec.network!r}")
        env_dir, docker_image, name = await asyncio.to_thread(self._definition, spec.image)
        sid = f"hb-{uuid.uuid4().hex}"
        trial_dir = os.path.join(self._root, "trials", sid)
        os.makedirs(trial_dir, mode=0o700)
        mode = h.NetworkMode.NO_NETWORK if spec.network == NETWORK_NONE else h.NetworkMode.PUBLIC
        config = h.EnvironmentConfig(docker_image=docker_image, cpus=max(1, math.ceil(float(spec.cpu))),
                                     memory_mb=int(spec.memory_mb), gpus=0, workdir=spec.workdir, network_mode=mode)

        def construct():
            return h.EnvironmentFactory.create_environment(
                type=h.type, environment_dir=Path(env_dir), environment_name=name, session_id=f"{name}__{sid[3:15]}",
                trial_paths=h.TrialPaths(trial_dir=Path(trial_dir)), task_env_config=config, logger=log,
                persistent_env=dict(spec.env or {}), mounts=[], network_policy=h.NetworkPolicy(network_mode=mode),
                **self.kwargs)

        try:
            env = await asyncio.to_thread(construct)
            if spec.network == NETWORK_NONE and not env.capabilities.disable_internet:
                raise RuntimeError(f"Harbor's {self.env_type} environment cannot block the network")
        except BaseException:
            shutil.rmtree(trial_dir, ignore_errors=True)
            raise
        try:
            await env.start(force_build=False)
        except BaseException as exc:
            self._spawn(self._discard(env, trial_dir))
            if isinstance(exc, Exception) and _is_build_failure(exc):
                raise ImageBuildError(str(exc)) from exc
            raise
        self._envs[sid] = env
        self._trials[sid] = trial_dir
        if spec.workdir:
            self._workdirs[sid] = spec.workdir
        return sid

    def _spawn(self, coro) -> None:
        task = asyncio.ensure_future(coro)
        self._background.add(task)
        task.add_done_callback(self._background.discard)

    async def _discard(self, env, trial_dir: str | None) -> None:
        try:
            await asyncio.wait_for(env.stop(delete=True), 120)
        except Exception as exc:  # noqa: BLE001
            log.warning("could not stop a harbor environment: %s", exc)
        finally:
            if trial_dir:
                shutil.rmtree(trial_dir, ignore_errors=True)

    def _env(self, sandbox_id: str):
        env = self._envs.get(sandbox_id)
        if env is None:
            raise KeyError(sandbox_id)
        return env

    async def _run(self, env, command: str, timeout_s: int = 60):
        result = await env.exec(command, timeout_sec=timeout_s)
        if result.return_code != 0:
            raise RuntimeError(f"{command!r} exited {result.return_code}: "
                               f"{((result.stderr or '') + (result.stdout or ''))[-500:]}")
        return result

    async def _upload(self, env, path: str, data: bytes) -> None:
        parent = posixpath.dirname(path)
        if parent and parent != "/":
            await self._run(env, f"mkdir -p -- {shlex.quote(parent)}")
        fd, local = tempfile.mkstemp(dir=os.path.join(self._root, "tmp"))
        try:
            with os.fdopen(fd, "wb") as f:
                await asyncio.to_thread(f.write, data)
            await env.upload_file(local, path)
        finally:
            os.unlink(local)

    async def exec(self, sandbox_id, argv, *, timeout_s, workdir, env, stdin, on_output: OutputCallback):
        henv = self._env(sandbox_id)
        stdin_path = f"{STDIN_DIR}/{uuid.uuid4().hex}" if stdin is not None else None
        try:
            if stdin_path:
                await self._upload(henv, stdin_path, stdin)
            command = build_command(list(argv), stdin_path)
            streamed = {"stdout": False, "stderr": False}

            async def relay(text, stream):
                if text:
                    fd = stream if stream in streamed else "stdout"
                    streamed[fd] = True
                    await on_output(fd, text.encode("utf-8", "replace") if isinstance(text, str) else bytes(text))

            t0 = time.monotonic()
            try:
                with henv.scoped_output_callback(relay):
                    result = await asyncio.wait_for(
                        henv.exec(command, cwd=workdir or self._workdirs.get(sandbox_id), env=env or None,
                                  timeout_sec=int(timeout_s)),
                        timeout_s + EXEC_GRACE_S)
            except Exception as exc:
                if _is_timeout(exc) and time.monotonic() - t0 >= timeout_s - 1:
                    return ExecOutcome(returncode=-1, timed_out=True)
                raise
            for fd, text in (("stdout", result.stdout), ("stderr", result.stderr)):
                if text and not streamed[fd]:
                    await on_output(fd, text.encode("utf-8", "replace"))
            rc = int(result.return_code)
            if rc == TIMEOUT_RC and time.monotonic() - t0 >= timeout_s - 1:
                return ExecOutcome(returncode=-1, timed_out=True)
            return ExecOutcome(returncode=rc, timed_out=False)
        finally:
            if stdin_path:
                try:
                    await henv.exec(f"rm -f -- {shlex.quote(stdin_path)}", timeout_sec=60)
                except Exception:  # noqa: BLE001
                    pass

    async def write_file(self, sandbox_id, path, data, mode):
        henv = self._env(sandbox_id)
        await self._upload(henv, path, data)
        if mode is not None:
            await self._run(henv, f"chmod {format(mode, 'o')} -- {shlex.quote(path)}")

    async def read_file(self, sandbox_id, path, max_bytes):
        henv = self._env(sandbox_id)
        q = shlex.quote(path)
        result = await henv.exec(f"test -f {q} || exit 3; wc -c < {q}", timeout_sec=60)
        if result.return_code == 3:
            raise FileNotFoundError(path)
        if result.return_code != 0:
            raise RuntimeError(f"cannot stat {path}: exit {result.return_code}: {(result.stderr or '')[-500:]}")
        if int((result.stdout or "0").strip() or 0) > max_bytes:
            raise FileTooLarge(path)
        fd, local = tempfile.mkstemp(dir=os.path.join(self._root, "tmp"))
        os.close(fd)
        try:
            await henv.download_file(path, local)
            data = await asyncio.to_thread(Path(local).read_bytes)
        finally:
            os.unlink(local)
        if len(data) > max_bytes:
            raise FileTooLarge(path)
        return data

    async def terminate(self, sandbox_id):
        henv = self._envs.pop(sandbox_id, None)
        trial_dir = self._trials.pop(sandbox_id, None)
        self._workdirs.pop(sandbox_id, None)
        self._poll_failures.pop(sandbox_id, None)
        if henv is None:
            return
        try:
            await henv.stop(delete=True)
        finally:
            if trial_dir:
                shutil.rmtree(trial_dir, ignore_errors=True)

    async def forget(self, sandbox_id: str) -> None:
        if sandbox_id in self._envs:  # ended without terminate (failed polls): release it on the platform
            try:
                await self.terminate(sandbox_id)
            except Exception as exc:  # noqa: BLE001
                log.warning("could not stop %s: %s", sandbox_id, exc)

    async def poll(self, sandbox_id):
        henv = self._envs.get(sandbox_id)
        if henv is None:
            return 0
        try:
            result = await henv.exec("true", timeout_sec=30)
        except Exception:
            failures = self._poll_failures.get(sandbox_id, 0) + 1
            self._poll_failures[sandbox_id] = failures
            if failures >= POLL_FAILURES:
                return 1
            raise
        self._poll_failures.pop(sandbox_id, None)
        return None if result.return_code == 0 else 1
