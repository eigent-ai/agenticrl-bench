from __future__ import annotations
import asyncio
import logging
import math
import posixpath
import shlex
import uuid
from typing import Any, Mapping
from .base import (NETWORK_EGRESS, NETWORK_NONE, Backend, CreateSpec, ExecOutcome, FileTooLarge, ImageBuildError,
                   ImageSpec, OutputCallback)
log = logging.getLogger("sandbox_broker.daytona")
SETTINGS = {"api_url", "target", "create_timeout_s", "disk_gb", "hostname"}
DEFAULT_DISK_GB = 10
STDIN_DIR = "/tmp/.sandbox-gate-stdin"
EXIT_POLL_S = 0.2
EXIT_WAIT_S = 30.0
RUNNING_STATES = {"started", "starting", "creating", "restoring", "pending_build", "building_snapshot",
                  "pulling_snapshot", "resizing", "snapshotting"}
def _minutes(seconds: float) -> int:
    return max(1, math.ceil(float(seconds) / 60))
def build_create_kwargs(spec: CreateSpec, *, disk_gb: int | None = None) -> dict[str, Any]:
    if spec.network not in (NETWORK_NONE, NETWORK_EGRESS):
        raise ValueError(f"unsupported network mode {spec.network!r}")
    resources = {"cpu": max(1, math.ceil(float(spec.cpu))), "memory": max(1, math.ceil(int(spec.memory_mb) / 1024))}
    if disk_gb:
        resources["disk"] = int(disk_gb)
    kwargs: dict[str, Any] = {
        "resources": resources,
        "network_block_all": spec.network == NETWORK_NONE,
        "public": False,
        "ephemeral": True,
        "ttl_minutes": _minutes(spec.timeout_s),
        "auto_stop_interval": _minutes(spec.idle_timeout_s) if spec.idle_timeout_s else 0,
    }
    if spec.env:
        kwargs["env_vars"] = dict(spec.env)
    if spec.tags:
        kwargs["labels"] = {str(k): str(v) for k, v in spec.tags.items()}
    return kwargs
def build_command(argv: list[str], *, workdir: str | None, env: dict[str, str] | None,
                  stdin_path: str | None) -> str:
    if not argv:
        raise ValueError("empty argv")
    parts = []
    if workdir:
        parts.append(f"cd -- {shlex.quote(workdir)} &&")
    if env:
        if "=" in argv[0]:
            raise ValueError("argv[0] must not contain '='")
        parts.append("env")
        parts += [shlex.quote(f"{k}={v}") for k, v in env.items()]
    parts.append(shlex.join(argv))
    parts.append(f"< {shlex.quote(stdin_path)}" if stdin_path else "< /dev/null")
    return " ".join(parts)
def _is_build_failure(exc: BaseException) -> bool:
    text = str(exc).lower()
    return "build_failed" in text or "failed to build" in text or "build failed" in text
def _is_not_found(exc: BaseException) -> bool:
    if any(t.__name__ == "DaytonaNotFoundError" for t in type(exc).__mro__):
        return True
    text = str(exc).lower()
    return "not found" in text or "no such file" in text
SET_HOSTNAME = 'hostname "$1" && printf "%s\\n" "$1" > /etc/hostname'
class DaytonaBackend(Backend):
    name = "daytona"
    native_hostname = True
    network_modes = (NETWORK_NONE, NETWORK_EGRESS)
    @classmethod
    def from_config(cls, settings: Mapping[str, Any], credentials: Mapping[str, Any], *,
                    state_dir: str) -> "DaytonaBackend":
        provider = dict(settings.get("settings") or {})
        unknown = set(provider) - SETTINGS
        if unknown:
            raise ValueError(f"unknown [daytona] key(s): {', '.join(sorted(unknown))}")
        net = dict(settings.get("parent_network") or {})
        net.pop("extra_domains", None)
        if net:
            raise ValueError("the daytona backend does not manage this container's allowlist; "
                             "remove [daytona.parent_network]")
        api_key = credentials.get("api_key")
        jwt = (credentials.get("jwt_token"), credentials.get("organization_id"))
        if not api_key and not all(jwt):
            raise ValueError("daytona backend needs api_key (or jwt_token and organization_id) credentials")
        return cls(api_key=api_key, jwt_token=jwt[0], organization_id=jwt[1],
                   api_url=provider.get("api_url"), target=provider.get("target") or credentials.get("target"),
                   create_timeout_s=float(provider.get("create_timeout_s", 900)),
                   disk_gb=int(provider.get("disk_gb") or DEFAULT_DISK_GB), hostname=provider.get("hostname"))
    def __init__(self, *, api_key: str | None = None, jwt_token: str | None = None,
                 organization_id: str | None = None, api_url: str | None = None, target: str | None = None,
                 create_timeout_s: float = 900.0, disk_gb: int | None = DEFAULT_DISK_GB,
                 hostname: str | None = None):
        self._auth = {"api_key": api_key, "jwt_token": jwt_token, "organization_id": organization_id}
        self.api_url = api_url or None
        self.target = target or None
        self.create_timeout_s = create_timeout_s
        self.disk_gb = disk_gb
        self.hostname = hostname or None
        self._sdk = None
        self._client = None
        self._sandboxes: dict[str, Any] = {}
        self._workdirs: dict[str, str] = {}
        self._hostnames: dict[str, str] = {}
        self._images: dict[tuple, Any] = {}
    async def start(self) -> None:
        import daytona
        self._sdk = daytona
        auth = {k: v for k, v in self._auth.items() if v}
        self._auth = None
        config = daytona.DaytonaConfig(**auth, **({"api_url": self.api_url} if self.api_url else {}),
                                       **({"target": self.target} if self.target else {}))
        self._client = daytona.AsyncDaytona(config)
        try:
            await self._client.get(f"sandbox-gate-probe-{uuid.uuid4().hex}")
        except Exception as exc:
            if not _is_not_found(exc):
                raise
    async def close(self) -> None:
        self._sandboxes.clear()
        if self._client is not None:
            try:
                await self._client.close()
            except Exception as exc:
                log.warning("closing the daytona client failed: %s", exc)
    def _image(self, spec: ImageSpec):
        img = self._images.get(spec.cache_key)
        if img is None:
            Image = self._sdk.Image
            if spec.kind == "registry":
                img = Image.base(spec.pull_ref)
            elif spec.kind == "context":
                img = Image.from_dockerfile(posixpath.join(spec.context_dir, "Dockerfile"), strict_context=True)
            else:
                raise ValueError(f"unknown image kind {spec.kind}")
            if spec.setup_commands:
                img = img.run_commands(*spec.setup_commands)
            self._images[spec.cache_key] = img
        return img
    async def create(self, spec: CreateSpec) -> str:
        sdk = self._sdk
        kwargs = build_create_kwargs(spec, disk_gb=self.disk_gb)
        kwargs["resources"] = sdk.Resources(**kwargs["resources"])
        try:
            params = sdk.CreateSandboxFromImageParams(image=self._image(spec.image), **kwargs)
            sb = await self._client.create(params, timeout=self.create_timeout_s)
        except Exception as exc:
            if _is_build_failure(exc):
                raise ImageBuildError(str(exc)) from exc
            raise
        if spec.network == NETWORK_NONE and not getattr(sb, "network_block_all", True):
            await self._delete(sb)
            raise RuntimeError("daytona created the sandbox without network_block_all")
        self._sandboxes[sb.id] = sb
        if spec.workdir:
            self._workdirs[sb.id] = spec.workdir
        hostname = spec.hostname or self.hostname
        if hostname:
            try:
                await self._sh(sb, f"sh -c {shlex.quote(SET_HOSTNAME)} _ {shlex.quote(hostname)}")
            except Exception:
                await self.terminate(sb.id)
                raise
            self._hostnames[sb.id] = hostname
        return sb.id
    def sandbox_meta(self, sandbox_id: str) -> dict:
        meta = {}
        if self._workdirs.get(sandbox_id):
            meta["workdir"] = self._workdirs[sandbox_id]
        if self._hostnames.get(sandbox_id):
            meta["hostname"] = self._hostnames[sandbox_id]
        return meta
    async def attach(self, sandbox_id: str, meta: dict | None = None) -> bool:
        try:
            sb = await self._client.get(sandbox_id)
            if str(getattr(sb.state, "value", sb.state)) != "started":
                return False
        except Exception as exc:
            log.warning("could not re-attach %s: %s", sandbox_id, exc)
            return False
        self._sandboxes[sandbox_id] = sb
        if (meta or {}).get("workdir"):
            self._workdirs[sandbox_id] = meta["workdir"]
        if (meta or {}).get("hostname"):
            self._hostnames[sandbox_id] = meta["hostname"]
        return True
    async def forget(self, sandbox_id: str) -> None:
        self._sandboxes.pop(sandbox_id, None)
        self._workdirs.pop(sandbox_id, None)
        self._hostnames.pop(sandbox_id, None)
    def _sb(self, sandbox_id: str):
        sb = self._sandboxes.get(sandbox_id)
        if sb is None:
            raise KeyError(sandbox_id)
        return sb
    async def _sh(self, sb, command: str, timeout_s: int = 60) -> None:
        resp = await sb.process.exec(command, timeout=timeout_s)
        if int(resp.exit_code or 0) != 0:
            raise RuntimeError(f"{command!r} exited {resp.exit_code}: {(resp.result or '')[-500:]}")
    async def _upload(self, sb, path: str, data: bytes) -> None:
        parent = posixpath.dirname(path)
        if parent and parent != "/":
            await self._sh(sb, f"mkdir -p -- {shlex.quote(parent)}")
        await sb.fs.upload_file(data, path)
    async def exec(self, sandbox_id, argv, *, timeout_s, workdir, env, stdin, on_output: OutputCallback):
        sb = self._sb(sandbox_id)
        session = f"sg-{uuid.uuid4().hex}"
        stdin_path = f"{STDIN_DIR}/{session}" if stdin is not None else None
        await sb.process.create_session(session)
        try:
            if stdin_path:
                await self._upload(sb, stdin_path, stdin)
            if sandbox_id in self._hostnames:
                env = {"HOSTNAME": self._hostnames[sandbox_id], **(env or {})}
            command = build_command(list(argv), workdir=workdir or self._workdirs.get(sandbox_id), env=env,
                                    stdin_path=stdin_path)
            resp = await sb.process.execute_session_command(
                session, self._sdk.SessionExecuteRequest(command=command, run_async=True))
            if not resp.cmd_id:
                raise RuntimeError("daytona returned no command id")
            try:
                rc = await asyncio.wait_for(self._follow(sb, session, resp.cmd_id, on_output), timeout=timeout_s)
            except asyncio.TimeoutError:
                await self._drop_session(sb, session)
                return ExecOutcome(returncode=-1, timed_out=True)
        finally:
            if stdin_path:
                try:
                    await self._sh(sb, f"rm -f -- {shlex.quote(stdin_path)}")
                except Exception:
                    pass
        return ExecOutcome(returncode=rc, timed_out=False)
    async def _follow(self, sb, session: str, cmd_id: str, on_output: OutputCallback) -> int:
        async def out(chunk):
            if chunk:
                await on_output("stdout", chunk.encode() if isinstance(chunk, str) else chunk)
        async def err(chunk):
            if chunk:
                await on_output("stderr", chunk.encode() if isinstance(chunk, str) else chunk)
        await sb.process.get_session_command_logs_async(session, cmd_id, out, err)
        loop = asyncio.get_running_loop()
        deadline = loop.time() + EXIT_WAIT_S
        while True:
            cmd = await sb.process.get_session_command(session, cmd_id)
            if cmd.exit_code is not None:
                return int(cmd.exit_code)
            if loop.time() > deadline:
                raise RuntimeError("daytona reported no exit code after the output ended")
            await asyncio.sleep(EXIT_POLL_S)
    async def _drop_session(self, sb, session: str) -> None:
        try:
            await sb.process.delete_session(session)
        except Exception as exc:
            log.warning("could not delete session %s: %s", session, exc)
    async def write_file(self, sandbox_id, path, data, mode):
        sb = self._sb(sandbox_id)
        await self._upload(sb, path, data)
        if mode is not None:
            await self._sh(sb, f"chmod {format(mode, 'o')} -- {shlex.quote(path)}")
    async def read_file(self, sandbox_id, path, max_bytes):
        sb = self._sb(sandbox_id)
        try:
            info = await sb.fs.get_file_info(path)
        except Exception as exc:
            if _is_not_found(exc):
                raise FileNotFoundError(path) from exc
            raise
        if info.is_dir:
            raise FileNotFoundError(path)
        if info.size > max_bytes:
            raise FileTooLarge(path)
        return await sb.fs.download_file(path)
    async def _delete(self, sb) -> None:
        try:
            await sb.delete()
        except Exception as exc:
            if not _is_not_found(exc):
                raise
    async def terminate(self, sandbox_id):
        sb = self._sandboxes.pop(sandbox_id, None)
        self._workdirs.pop(sandbox_id, None)
        self._hostnames.pop(sandbox_id, None)
        if sb is None:
            try:
                sb = await self._client.get(sandbox_id)
            except Exception as exc:
                if _is_not_found(exc):
                    return
                raise
        await self._delete(sb)
    async def poll(self, sandbox_id):
        sb = self._sandboxes.get(sandbox_id)
        if sb is None:
            return 0
        try:
            await sb.refresh_data()
        except Exception as exc:
            if not _is_not_found(exc):
                raise
            self._sandboxes.pop(sandbox_id, None)
            return 0
        state = str(getattr(sb.state, "value", sb.state))
        if state in RUNNING_STATES:
            return None
        self._sandboxes.pop(sandbox_id, None)
        return 1 if state in ("error", "build_failed") else 0
