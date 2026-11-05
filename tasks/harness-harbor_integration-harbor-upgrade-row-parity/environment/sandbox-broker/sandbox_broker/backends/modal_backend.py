"""Modal backend (the reference backend): CPU sandboxes, outbound networking blocked by default.

Root-only backend config (``provider = "modal"``)::

    [settings]
    app_name = "sandbox-gate"          # Modal app the sandboxes are created under
    environment = "main"               # Modal environment (or SANDBOX_GATE_PROVIDER_ENV at start)

    [parent_network]                   # optional: narrow this container's own allowlist
    manage_allowlist = false
    domains = ["api.modal.com"]
    cidrs = []
    refresh_interval_s = 60

Hostname: Modal 1.6.1 has no create-time hostname option, so ``native_hostname`` is False
and the gate's fallback applies (see BACKENDS.md, "Hostname normalisation").
"""
from __future__ import annotations

import asyncio
import dataclasses
import logging
import os
import posixpath
import ssl
import time
from typing import Any, Mapping
from urllib.parse import urlparse

from .base import (NETWORK_EGRESS, NETWORK_NONE, Backend, CreateSpec, ExecOutcome, FileTooLarge, ImageBuildError,
                   ImageSpec, OutputCallback)

log = logging.getLogger("sandbox_broker.modal")

KEEPALIVE = ("sh", "-c", "sleep infinity")


@dataclasses.dataclass
class ParentNetwork:
    """Outbound rules of the container the daemon runs in (not of the sandboxes it creates).

    With ``manage_allowlist`` the backend keeps this container's outbound allowlist at
    ``domains`` plus the exact command-router hosts it needs (this container's own, and one
    per live sandbox) instead of a ``*.w.modal.host`` wildcard, which also covers every public
    Modal tunnel. The container must start with the wildcard allowed (the backend uses it once
    to reach its own router) and the credentials must be allowed to modify this container.
    """

    manage_allowlist: bool = False
    domains: list[str] = dataclasses.field(default_factory=lambda: ["api.modal.com"])
    cidrs: list[str] = dataclasses.field(default_factory=list)
    refresh_interval_s: float = 60.0


def build_create_kwargs(spec: CreateSpec) -> dict[str, Any]:
    """Keyword arguments for ``modal.Sandbox.create`` (without app/image/client).

    Networking is fixed here: ``block_network=True`` unless the operator's policy asked for
    egress, and never anything that could open a path in (no ports, tunnels, volumes, secrets
    or GPUs).
    """
    if spec.network not in (NETWORK_NONE, NETWORK_EGRESS):
        raise ValueError(f"unsupported network mode {spec.network!r}")
    kwargs: dict[str, Any] = {
        "timeout": int(spec.timeout_s),
        "cpu": (float(spec.cpu), float(spec.cpu)),
        "memory": (int(spec.memory_mb), int(spec.memory_mb)),
        "block_network": spec.network == NETWORK_NONE,
    }
    if spec.idle_timeout_s:
        kwargs["idle_timeout"] = int(spec.idle_timeout_s)
    if spec.workdir:
        kwargs["workdir"] = spec.workdir
    if spec.env:
        kwargs["env"] = dict(spec.env)
    if spec.tags:
        kwargs["tags"] = dict(spec.tags)
    return kwargs


class ModalBackend(Backend):
    name = "modal"
    native_hostname = False
    network_modes = (NETWORK_NONE, NETWORK_EGRESS)

    @classmethod
    def from_config(cls, settings: Mapping[str, Any], credentials: Mapping[str, Any], *,
                    state_dir: str) -> "ModalBackend":
        provider = dict(settings.get("settings") or {})
        unknown = set(provider) - {"app_name", "environment"}
        if unknown:
            raise ValueError(f"unknown [settings] key(s) for modal: {', '.join(sorted(unknown))}")
        net = dict(settings.get("parent_network") or {})
        extra = net.pop("extra_domains", [])
        fields = {f.name for f in dataclasses.fields(ParentNetwork)}
        if set(net) - fields:
            raise ValueError(f"unknown [parent_network] key(s): {', '.join(sorted(set(net) - fields))}")
        if not credentials.get("token_id") or not credentials.get("token_secret"):
            raise ValueError("modal backend needs token_id and token_secret credentials")
        network = ParentNetwork(**net)
        # hosts a run's harness needs (agent model API, ...) are a run-time choice: SANDBOX_GATE_EXTRA_PARENT_DOMAINS
        network.domains = list(dict.fromkeys([*network.domains, *extra]))
        return cls(credentials["token_id"], credentials["token_secret"], provider.get("app_name") or "sandbox-gate",
                   provider.get("environment") or credentials.get("environment"),
                   parent_sandbox_id=credentials.get("parent_sandbox_id"), network=network)

    @classmethod
    def capture_runtime(cls, env: Mapping[str, str]) -> dict[str, str]:
        # this container's own sandbox id, needed only to manage its allowlist
        return {"parent_sandbox_id": env["MODAL_SANDBOX_ID"]} if env.get("MODAL_SANDBOX_ID") else {}

    @property
    def maintain_interval_s(self) -> float:
        return float(self._network.refresh_interval_s) if self._network is not None else 60.0

    def __init__(self, token_id: str, token_secret: str, app_name: str,
                 environment_name: str | None = None, *, parent_sandbox_id: str | None = None,
                 network: ParentNetwork | None = None):
        self._token = (token_id, token_secret)
        self.app_name = app_name
        self.environment_name = environment_name or None
        self._modal = None
        self._client = None
        self._app = None
        self._sandboxes: dict[str, Any] = {}
        self._images: dict[tuple, Any] = {}
        self._image_lock = asyncio.Lock()
        self._network = network
        self._parent_id = parent_sandbox_id or None
        self._parent = None
        self._router_hosts: dict[str, str] = {}
        self._own_router_host: str | None = None
        self._applied: tuple | None = None
        self._net_lock = asyncio.Lock()

    @property
    def manages_parent_network(self) -> bool:
        return bool(self._network is not None and self._network.manage_allowlist)

    async def start(self) -> None:
        import modal

        self._modal = modal
        token_id, token_secret = self._token
        self._token = None
        self._client = await modal.Client.from_credentials.aio(token_id, token_secret)
        self._app = await modal.App.lookup.aio(self.app_name, create_if_missing=True, client=self._client,
                                               environment_name=self.environment_name)
        if self.manages_parent_network:
            if not self._parent_id:
                raise RuntimeError("manage_allowlist needs this container's sandbox id (MODAL_SANDBOX_ID)")
            self._parent = await modal.Sandbox.from_id.aio(self._parent_id, client=self._client)
            self._own_router_host = await self._find_own_router_host()
            await self._apply_parent_policy(force=True)

    # -------------------------------------------------------------- parent allowlist

    @staticmethod
    def _router_host(sb) -> str | None:
        """Hostname of the sandbox's command router (``task-<id>.w.modal.host``), known right after create."""
        try:
            from modal._utils.async_utils import synchronizer

            impl = synchronizer._translate_in(sb)
            url = getattr(getattr(impl, "_init_command_router_access", None), "url", None)
            if not url and getattr(impl, "_command_router_client", None) is not None:
                url = impl._command_router_client._server_url
            return urlparse(url).hostname if url else None
        except Exception:  # noqa: BLE001
            return None

    async def _find_own_router_host(self) -> str:
        """Modal applies a sandbox's network policy through that sandbox's own command router, so
        this container must keep its own router host reachable. The container therefore has to
        start with ``*.w.modal.host`` allowed: re-applying that starting policy opens the router
        connection, which tells us the host; the next update narrows the list."""
        from modal._utils.async_utils import synchronizer

        starting = sorted(set(self._network.domains) | {"*.w.modal.host"})
        try:
            await asyncio.wait_for(self._parent._experimental_set_outbound_network_policy.aio(
                outbound_domain_allowlist=starting, outbound_cidr_allowlist=list(self._network.cidrs)), 45)
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(
                "cannot reach this container's own command router; start the container with "
                "'*.w.modal.host' in its allowlist (the broker narrows it to exact hosts) "
                f"or turn off manage_allowlist ({type(exc).__name__}: {exc})") from exc
        router = getattr(synchronizer._translate_in(self._parent), "_command_router_client", None)
        host = urlparse(getattr(router, "_server_url", "") or "").hostname
        if not host:
            raise RuntimeError("could not determine this container's command router host")
        return host

    async def _apply_parent_policy(self, force: bool = False) -> None:
        async with self._net_lock:
            own = {self._own_router_host} if self._own_router_host else set()
            domains = sorted(set(self._network.domains) | own | set(self._router_hosts.values()))
            key = (tuple(domains), tuple(self._network.cidrs))
            if key == self._applied and not force:
                return
            await self._parent._experimental_set_outbound_network_policy.aio(
                outbound_domain_allowlist=domains, outbound_cidr_allowlist=list(self._network.cidrs))
            self._applied = key

    @staticmethod
    async def _wait_reachable(host: str, timeout_s: float = 20.0) -> float:
        """Wait until a TLS handshake with ``host`` succeeds (the new allowlist entry is in effect)."""
        t0 = time.monotonic()
        ctx = ssl.create_default_context()
        while True:
            try:
                _, w = await asyncio.wait_for(asyncio.open_connection(host, 443, ssl=ctx, server_hostname=host), 5)
                w.close()
                return time.monotonic() - t0
            except (OSError, asyncio.TimeoutError, ssl.SSLError):
                if time.monotonic() - t0 > timeout_s:
                    raise
                await asyncio.sleep(0.25)

    async def _allow_router(self, sandbox_id: str, sb) -> None:
        host = self._router_host(sb)
        if not host:
            log.warning("router host of %s is unknown; exec will fail until it is allowed", sandbox_id)
            return
        self._router_hosts[sandbox_id] = host
        await self._apply_parent_policy()
        try:
            waited = await self._wait_reachable(host)
            log.info("router %s reachable after %.2fs", host, waited)
        except Exception as exc:  # noqa: BLE001
            log.warning("router %s not reachable yet: %s", host, exc)

    def sandbox_meta(self, sandbox_id: str) -> dict:
        host = self._router_hosts.get(sandbox_id)
        return {"router_host": host} if host else {}

    async def forget(self, sandbox_id: str) -> None:
        self._sandboxes.pop(sandbox_id, None)
        if self._router_hosts.pop(sandbox_id, None) and self.manages_parent_network:
            await self._apply_parent_policy()

    async def maintain(self) -> None:
        if self.manages_parent_network:
            await self._apply_parent_policy(force=True)

    async def _image(self, spec: ImageSpec):
        async with self._image_lock:
            img = self._images.get(spec.cache_key)
            if img is None:
                modal = self._modal
                if spec.kind == "registry":
                    img = modal.Image.from_registry(spec.pull_ref)
                elif spec.kind == "context":
                    img = modal.Image.from_dockerfile(os.path.join(spec.context_dir, "Dockerfile"),
                                                      context_dir=spec.context_dir)
                else:
                    raise ValueError(f"unknown image kind {spec.kind}")
                if spec.setup_commands:
                    img = img.run_commands(*spec.setup_commands)
                self._images[spec.cache_key] = img
            return img

    async def create(self, spec: CreateSpec) -> str:
        image = await self._image(spec.image)
        try:
            sb = await self._modal.Sandbox.create.aio(*KEEPALIVE, app=self._app, image=image, client=self._client,
                                                      **build_create_kwargs(spec))
        except Exception as exc:  # noqa: BLE001
            # modal.exception.ImageBuildError (lazy image builds surface at create); matched by name so this
            # module never needs the SDK at import time
            if any("ImageBuild" in t.__name__ for t in type(exc).__mro__):
                raise ImageBuildError(str(exc)) from exc
            raise
        self._sandboxes[sb.object_id] = sb
        if self.manages_parent_network:
            await self._allow_router(sb.object_id, sb)
        return sb.object_id

    async def attach(self, sandbox_id: str, meta: dict | None = None) -> bool:
        try:
            sb = await self._modal.Sandbox.from_id.aio(sandbox_id, client=self._client)
            if await sb.poll.aio() is not None:
                return False
        except Exception as exc:  # noqa: BLE001
            log.warning("could not re-attach %s: %s", sandbox_id, exc)
            return False
        self._sandboxes[sandbox_id] = sb
        if self.manages_parent_network and (meta or {}).get("router_host"):
            self._router_hosts[sandbox_id] = meta["router_host"]
            await self._apply_parent_policy()
        return True

    def _sb(self, sandbox_id: str):
        sb = self._sandboxes.get(sandbox_id)
        if sb is None:
            raise KeyError(sandbox_id)
        return sb

    async def exec(self, sandbox_id, argv, *, timeout_s, workdir, env, stdin, on_output: OutputCallback):
        sb = self._sb(sandbox_id)
        proc = await sb.exec.aio(*argv, timeout=int(timeout_s), workdir=workdir, env=env or None, text=False)
        if stdin is not None:
            proc.stdin.write(stdin)
            proc.stdin.write_eof()
            await proc.stdin.drain.aio()

        async def pump(stream, fd):
            async for chunk in stream:
                if chunk:
                    await on_output(fd, chunk if isinstance(chunk, bytes) else chunk.encode())

        await asyncio.gather(pump(proc.stdout, "stdout"), pump(proc.stderr, "stderr"))
        rc = await proc.wait.aio()
        rc = -1 if rc is None else int(rc)
        return ExecOutcome(returncode=rc, timed_out=rc == -1)

    async def write_file(self, sandbox_id, path, data, mode):
        sb = self._sb(sandbox_id)
        parent = posixpath.dirname(path)
        if parent and parent != "/":
            await sb.filesystem.make_directory.aio(parent, create_parents=True)
        await sb.filesystem.write_bytes.aio(data, path)
        if mode is not None:
            p = await sb.exec.aio("chmod", format(mode, "o"), path, timeout=60)
            await p.wait.aio()

    async def read_file(self, sandbox_id, path, max_bytes):
        sb = self._sb(sandbox_id)
        try:
            info = await sb.filesystem.stat.aio(path)
        except Exception as exc:  # noqa: BLE001
            # modal.exception.SandboxFilesystemNotFoundError (not NotFoundError, which means the sandbox is gone);
            # matched by name so this module never needs the SDK at import time
            if any(t.__name__ == "SandboxFilesystemNotFoundError" for t in type(exc).__mro__):
                raise FileNotFoundError(path) from exc
            raise
        if str(getattr(getattr(info, "type", None), "value", "")) == "directory":
            raise FileNotFoundError(path)  # as on every other backend: only regular files are read
        if info.size > max_bytes:
            raise FileTooLarge(path)
        return await sb.filesystem.read_bytes.aio(path)

    async def terminate(self, sandbox_id):
        sb = self._sandboxes.pop(sandbox_id, None)
        if sb is None:
            sb = await self._modal.Sandbox.from_id.aio(sandbox_id, client=self._client)
        await sb.terminate.aio()

    async def poll(self, sandbox_id):
        sb = self._sandboxes.get(sandbox_id)
        if sb is None:
            return 0
        rc = await sb.poll.aio()
        if rc is not None:
            self._sandboxes.pop(sandbox_id, None)
        return rc

    async def close(self) -> None:
        self._sandboxes.clear()
