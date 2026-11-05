"""The gate daemon: a Unix-socket API in front of a sandbox backend.

The daemon owns the platform credentials. Clients only see the operations in
``protocol.py``; every limit is enforced here, whatever the client sends.

Platform neutrality towards non-admin clients (the workload):
  * sandbox ids are the gate's own (``sbx-<hex>``), never the platform's;
  * replies, errors and the world-readable audit log never carry backend names, platform
    ids or platform error text; failures get a reference (``ref``) whose details go to the
    root-only daemon log (admins, e.g. a root verifier, also get them in the reply);
  * every sandbox gets the policy's hostname (natively, or through HOSTNAME_FALLBACK);
  * every sandbox gets the same runtime environment variables (RUNTIME_ENV) on every backend.
"""
from __future__ import annotations

import asyncio
import base64
import binascii
import codecs
import dataclasses
import io
import json
import logging
import os
import re
import shutil
import signal
import socket
import stat
import struct
import tarfile
import time
import uuid
from typing import Any

from . import __version__
from .audit import AuditLog
from .backends.base import Backend, CreateSpec, FileTooLarge, ImageBuildError, ImageSpec
from .policy import Policy, hash_context_dir, resolve_registry_image
from .protocol import (ADMIN_OPS, PROTOCOL_VERSION, BackendFailure, BadRequest, BrokerError,
                       BrokerUnavailable, PolicyDenied, QuotaExceeded, SandboxNotFound, decode, encode,
                       validate_request)

log = logging.getLogger("sandbox_broker.server")

_LABEL_KEY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]{0,62}$")
_ENV_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,127}$")
_QUIET_OPS = {"ping", "usage", "policy", "poll", "list"}
_ENDED_KEEP = 2000

# Best-effort hostname normalisation for backends without native support: set the kernel hostname
# where the sandbox allows it (root with CAP_SYS_ADMIN in its UTS namespace) and /etc/hostname.
HOSTNAME_FALLBACK = ('h="$1"; hostname "$h" 2>/dev/null; '
                     '[ -w /etc/hostname ] && printf "%s\\n" "$h" > /etc/hostname 2>/dev/null; true')


# The runtime environment every sandbox gets on every backend, so that programs see the same variables on every platform
# (hash seed, thread pools of BLAS/OpenMP libraries, terminal type, build defaults). These are the values the recorded
# runs had: Modal sets exactly these in its sandboxes, other platforms set none of them (a Daytona sandbox shows the
# host's 64 CPUs, so BLAS/OpenMP would start 64 threads in a 1-CPU sandbox). Set at creation, under the client's own
# ``env`` (an explicit client value wins). It overrides an image ENV of the same name; no pool image (nor any recorded
# submission's Dockerfile) sets one of these.
RUNTIME_ENV = {"PYTHONHASHSEED": "0", "PYTHONPATH": "/pkg/:/root/", "TERM": "xterm", "SOURCE_DATE_EPOCH": "1641013200",
               "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "BLIS_NUM_THREADS": "1",
               "ORT_INTER_OP_NUM_THREADS": "1", "ORT_INTRA_OP_NUM_THREADS": "1", "CFLAGS": "-g0",
               "PIP_DEFAULT_TIMEOUT": "30", "PIP_NO_CACHE_DIR": "off", "PIP_ROOT_USER_ACTION": "ignore",
               "SSL_CERT_DIR": "/etc/ssl/certs", "UV_BREAK_SYSTEM_PACKAGES": "1"}


def prompt_env(hostname: str) -> dict[str, str]:
    """Environment that makes interactive bash prompts show ``hostname`` for \\h and \\H."""
    return {"HOSTNAME": hostname,
            "PROMPT_COMMAND": f"PS1=${{PS1//\\\\h/{hostname}}}; PS1=${{PS1//\\\\H/{hostname}}}"}


@dataclasses.dataclass
class Peer:
    pid: int
    uid: int
    gid: int

    def as_dict(self) -> dict[str, int]:
        return {"pid": self.pid, "uid": self.uid, "gid": self.gid}


@dataclasses.dataclass
class SandboxRecord:
    id: str  # the gate's id (what clients see)
    owner_uid: int
    image: str
    cpu: float
    memory_mb: int
    timeout_s: int
    idle_timeout_s: int | None
    created_at: float
    deadline: float
    labels: dict[str, str] = dataclasses.field(default_factory=dict)
    meta: dict[str, Any] = dataclasses.field(default_factory=dict)
    execs: int = 0
    ended_at: float | None = None
    end_reason: str | None = None
    returncode: int | None = None
    backend_id: str = ""  # the platform's id (never shown to clients)

    def __post_init__(self) -> None:
        if not self.backend_id:  # state files written before gate ids existed
            self.backend_id = self.id

    def lifetime(self, now: float) -> float:
        return max(0.0, (self.ended_at or now) - self.created_at)

    def public(self, now: float, network: str = "blocked") -> dict[str, Any]:
        d = dataclasses.asdict(self)
        d.pop("meta", None)
        d.pop("backend_id", None)
        d["running"] = self.ended_at is None
        d["lifetime_s"] = round(self.lifetime(now), 1)
        d["network"] = network
        return d


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _unb64(value: Any, field: str) -> bytes:
    if not isinstance(value, str):
        raise BadRequest(f"{field} must be a base64 string")
    try:
        return base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise BadRequest(f"{field} is not valid base64") from exc


def _abs_path(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.startswith("/") or "\0" in value or len(value) > 4096:
        raise BadRequest(f"{field} must be an absolute path")
    return value


def _str_map(value: Any, field: str, *, key_re: re.Pattern, max_items: int, max_value: int) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict) or len(value) > max_items:
        raise BadRequest(f"{field} must be an object with at most {max_items} entries")
    out = {}
    for k, v in value.items():
        if not isinstance(k, str) or not key_re.match(k):
            raise BadRequest(f"invalid key in {field}: {k!r}")
        if not isinstance(v, str) or len(v) > max_value or "\0" in v:
            raise BadRequest(f"invalid value in {field} for {k!r}")
        out[k] = v
    return out


def _number(req: dict, key: str, default, lo, hi, kind=float):
    v = req.get(key)
    if v is None:
        return kind(default)
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise BadRequest(f"{key} must be a number")
    if v < lo or v > hi:
        raise PolicyDenied(f"{key}={v} is outside the allowed range [{lo}, {hi}]")
    return kind(v)


def _timeout(req: dict, key: str, default: int, hi: int) -> int:
    v = req.get(key)
    if v is None:
        v = default
    if isinstance(v, bool) or not isinstance(v, (int, float)) or v <= 0:
        raise BadRequest(f"{key} must be a positive number")
    return int(min(max(1, int(v)), hi))


def _short_argv(argv: list[str], limit: int = 2000) -> str:
    text = json.dumps(argv, ensure_ascii=False)
    return text if len(text) <= limit else text[:limit] + f"...(+{len(text) - limit} chars)"


def safe_extract_context(data: bytes, dest: str, max_bytes: int, max_members: int = 10000,
                         max_file_bytes: int | None = None) -> None:
    """Extract a tar(.gz) build context, refusing links, devices and paths that escape ``dest``."""
    total = 0
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as tf:
        members = tf.getmembers()
        if len(members) > max_members:
            raise BadRequest("build context has too many files")
        for m in members:
            name = m.name
            while name.startswith("./"):
                name = name[2:]
            if not name or name == ".":
                continue
            parts = name.split("/")
            if name.startswith("/") or ".." in parts:
                raise BadRequest(f"unsafe path in build context: {m.name!r}")
            target = os.path.join(dest, *parts)
            if m.isdir():
                os.makedirs(target, mode=0o755, exist_ok=True)
            elif m.isreg():
                if max_file_bytes is not None and m.size > max_file_bytes:
                    raise PolicyDenied(f"build context file {name!r} is {m.size} bytes; the limit per file is "
                                       f"{max_file_bytes} (bake large files into a prebuilt image instead)")
                total += m.size
                if total > max_bytes * 4:
                    raise BadRequest("build context is too large when unpacked")
                os.makedirs(os.path.dirname(target), mode=0o755, exist_ok=True)
                src = tf.extractfile(m)
                with open(target, "wb") as out:
                    shutil.copyfileobj(src, out)
                os.chmod(target, 0o755 if m.mode & 0o111 else 0o644)
            else:
                raise BadRequest(f"build context may only contain regular files and directories: {m.name!r}")
    if not os.path.isfile(os.path.join(dest, "Dockerfile")):
        raise BadRequest("build context has no Dockerfile at its root")


class BrokerServer:
    def __init__(self, policy: Policy, backend: Backend, *, audit: AuditLog | None = None,
                 parent_id: str | None = None, clock=time.time):
        self.policy = policy
        self.limits = policy.limits
        self.backend = backend
        self.audit = audit or AuditLog(policy.audit_log, policy.audit_log_mode)
        self.clock = clock
        self.parent_id = parent_id or ""
        self.session_id = uuid.uuid4().hex[:12]
        self.started_at = clock()
        self.records: dict[str, SandboxRecord] = {}
        self.pending_creates = 0
        self.creates_total = 0
        self.failed_creates = 0
        self.denied_total = 0
        self.closed_seconds = 0.0
        self.peak_live = 0
        self.ready = False
        self.backend_error: str | None = None
        self.shutting_down = False
        self.budget_exhausted = False
        self._lock = asyncio.Lock()
        self._exec_sem = asyncio.Semaphore(self.limits.max_inflight_execs)
        self._stop = asyncio.Event()
        self._server: asyncio.AbstractServer | None = None
        self._tasks: list[asyncio.Task] = []
        self._last_usage_log = 0.0
        self._last_maintain = 0.0
        self._forget_later: set[str] = set()
        self.network_label = "blocked" if policy.sandbox.network == "none" else "egress"

    # ------------------------------------------------------------------ neutral errors

    def _fault(self, public: str, exc: BaseException | None = None) -> BackendFailure:
        """A BackendFailure whose message is platform-neutral; the details go to the root-only log."""
        ref = uuid.uuid4().hex[:8]
        detail = f"{type(exc).__name__}: {exc}" if exc is not None else ""
        log.warning("[ref %s] %s%s", ref, public, f": {detail}" if detail else "")
        err = BackendFailure(f"{public} (ref {ref})")
        err.detail = detail  # type: ignore[attr-defined]
        return err

    def _is_admin(self, peer: Peer) -> bool:
        return peer.uid in self.policy.admin_uids

    # ------------------------------------------------------------------ accounting

    def live(self) -> list[SandboxRecord]:
        return [r for r in self.records.values() if r.ended_at is None]

    def used_seconds(self, now: float | None = None) -> float:
        now = self.clock() if now is None else now
        return self.closed_seconds + sum(r.lifetime(now) for r in self.live())

    def budget_remaining(self, now: float | None = None) -> float | None:
        budget = self.limits.budget_sandbox_seconds
        if not budget:
            return None
        return max(0.0, budget - self.used_seconds(now))

    def usage(self) -> dict[str, Any]:
        now = self.clock()
        rem = self.budget_remaining(now)
        return {
            "session": self.session_id,
            "live": len(self.live()),
            "pending": self.pending_creates,
            "peak_live": self.peak_live,
            "max_concurrent": self.limits.max_concurrent,
            "creates_total": self.creates_total,
            "failed_creates": self.failed_creates,
            "denied_total": self.denied_total,
            "used_sandbox_seconds": round(self.used_seconds(now), 1),
            "budget_sandbox_seconds": self.limits.budget_sandbox_seconds or None,
            "remaining_sandbox_seconds": None if rem is None else round(rem, 1),
            "budget_exhausted": self.budget_exhausted,
            "uptime_s": round(now - self.started_at, 1),
        }

    def _end(self, rec: SandboxRecord, reason: str, rc: int | None = None) -> None:
        if rec.ended_at is not None:
            return
        rec.ended_at = self.clock()
        rec.end_reason = reason
        rec.returncode = rc
        self.closed_seconds += rec.lifetime(rec.ended_at)
        self._forget_later.add(rec.backend_id)
        self.audit.write("sandbox_ended", sandbox_id=rec.id, reason=reason, returncode=rc,
                         lifetime_s=round(rec.lifetime(rec.ended_at), 1), execs=rec.execs, owner_uid=rec.owner_uid)
        ended = [r for r in self.records.values() if r.ended_at is not None]
        if len(ended) > _ENDED_KEEP:
            for r in sorted(ended, key=lambda r: r.ended_at)[: len(ended) - _ENDED_KEEP]:
                self.records.pop(r.id, None)

    async def _terminate_rec(self, rec: SandboxRecord, reason: str) -> None:
        if rec.ended_at is not None:
            return
        try:
            await asyncio.wait_for(self.backend.terminate(rec.backend_id), 120)
        except Exception as exc:  # noqa: BLE001
            log.warning("terminate %s failed: %s", rec.id, exc)
        self._end(rec, reason)
        await self._flush_forgets()

    async def _flush_forgets(self) -> None:
        while self._forget_later:
            sid = self._forget_later.pop()
            try:
                await self.backend.forget(sid)
            except Exception as exc:  # noqa: BLE001
                log.warning("forget %s failed: %s", sid, exc)

    # ------------------------------------------------------------------ state

    def save_state(self) -> None:
        state = {
            "session_id": self.session_id,
            "started_at": self.started_at,
            "creates_total": self.creates_total,
            "failed_creates": self.failed_creates,
            "denied_total": self.denied_total,
            "closed_seconds": self.closed_seconds,
            "peak_live": self.peak_live,
            "budget_exhausted": self.budget_exhausted,
            "live": [dataclasses.asdict(r) for r in self.live()],
        }
        path = self.policy.state_path
        os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
        tmp = f"{path}.tmp"
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            json.dump(state, f)
        os.replace(tmp, path)

    async def load_state(self) -> None:
        path = self.policy.state_path
        if not os.path.exists(path):
            return
        try:
            with open(path) as f:
                state = json.load(f)
        except (OSError, ValueError) as exc:
            log.warning("ignoring unreadable state file: %s", exc)
            return
        self.session_id = state.get("session_id", self.session_id)
        self.started_at = state.get("started_at", self.started_at)
        self.creates_total = state.get("creates_total", 0)
        self.failed_creates = state.get("failed_creates", 0)
        self.denied_total = state.get("denied_total", 0)
        self.closed_seconds = state.get("closed_seconds", 0.0)
        self.peak_live = state.get("peak_live", 0)
        self.budget_exhausted = state.get("budget_exhausted", False)
        for d in state.get("live", []):
            rec = SandboxRecord(**d)
            self.records[rec.id] = rec
            if not await self.backend.attach(rec.backend_id, rec.meta):
                self._end(rec, "lost")
        await self._flush_forgets()
        self.audit.write("state_restored", live=len(self.live()), used_sandbox_seconds=round(self.used_seconds(), 1))

    # ------------------------------------------------------------------ connection handling

    @staticmethod
    def _peer(writer: asyncio.StreamWriter) -> Peer:
        sock = writer.get_extra_info("socket")
        try:
            raw = sock.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i"))
            pid, uid, gid = struct.unpack("3i", raw)
            return Peer(pid, uid, gid)
        except (AttributeError, OSError):
            return Peer(-1, -1, -1)

    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        peer = self._peer(writer)
        try:
            while True:
                try:
                    line = await reader.readline()
                except (ValueError, asyncio.LimitOverrunError):
                    writer.write(encode({"ok": False, "error": "request is too large", "error_type": "bad_request"}))
                    await writer.drain()
                    break
                if not line:
                    break
                if not line.strip():
                    continue
                reply = await self.process(line, peer, writer)
                writer.write(encode(reply))
                await writer.drain()
        except (ConnectionError, BrokenPipeError):
            pass
        finally:
            try:
                writer.close()
            except Exception:  # noqa: BLE001
                pass

    async def process(self, line: bytes, peer: Peer, writer: asyncio.StreamWriter | None = None) -> dict[str, Any]:
        t0 = time.monotonic()
        op = "?"
        detail = ""
        req: dict[str, Any] = {}
        fields: dict[str, Any] = {}
        outcome = "allowed"
        try:
            try:
                req = decode(line)
            except (ValueError, UnicodeDecodeError) as exc:
                raise BadRequest(f"malformed request: {exc}") from exc
            if isinstance(req.get("op"), str):
                op = req["op"][:32]
            op = validate_request(req)
            self._authorize(peer, op)
            handler = getattr(self, f"_op_{op}")
            result = await handler(req, peer, writer, fields)
            reply = {"ok": True, **result}
        except BrokerError as exc:
            outcome = "denied" if exc.kind in ("denied", "quota", "bad_request") else "failed"
            reply = {"ok": False, "error": str(exc), "error_type": exc.kind}
            detail = getattr(exc, "detail", "")
        except Exception as exc:  # noqa: BLE001
            log.exception("unexpected error in %s", op)
            outcome = "failed"
            fault = self._fault("internal error", exc)
            reply = {"ok": False, "error": str(fault), "error_type": "backend"}
            detail = fault.detail  # type: ignore[attr-defined]
        public_error = reply.get("error")
        if detail and self._is_admin(peer):
            reply["error"] = f"{reply['error']}: {detail}"
        if outcome == "denied":
            self.denied_total += 1
        if "request_id" in req:
            reply["request_id"] = req["request_id"]
        if op not in _QUIET_OPS or outcome != "allowed":
            extra = {"error": public_error} if not reply["ok"] else {}
            self.audit.write("request", op=op, peer=peer.as_dict(), outcome=outcome,
                             duration_ms=int((time.monotonic() - t0) * 1000), **fields, **extra)
        return reply

    def _authorize(self, peer: Peer, op: str) -> None:
        admins = self.policy.admin_uids
        allowed = self.policy.allowed_uids
        if allowed and peer.uid not in allowed and peer.uid not in admins and op != "ping":
            raise PolicyDenied("this user is not allowed to use the sandbox broker")
        if op in ADMIN_OPS and peer.uid not in admins:
            raise PolicyDenied(f"'{op}' is restricted to administrators")
        if op not in ("ping", "usage", "policy", "list", "poll", "shutdown") and not self.ready:
            state = "starting" if not self.backend_error else "unavailable"
            if self.backend_error and peer.uid in self.policy.admin_uids:
                state = self.backend_error
            raise BrokerUnavailable(f"sandbox backend is not ready: {state}")

    def _owned(self, req: dict, peer: Peer, *, allow_ended: bool = False) -> SandboxRecord:
        sid = req.get("id")
        if not isinstance(sid, str):
            raise BadRequest("missing sandbox 'id'")
        rec = self.records.get(sid)
        if rec is None or (rec.owner_uid != peer.uid and peer.uid not in self.policy.admin_uids):
            raise SandboxNotFound(f"no sandbox {sid!r}")
        if rec.ended_at is not None and not allow_ended:
            raise SandboxNotFound(f"sandbox {sid!r} has ended ({rec.end_reason})")
        return rec

    # ------------------------------------------------------------------ operations

    async def _op_ping(self, req, peer, writer, fields):
        reply = {"version": __version__, "protocol": PROTOCOL_VERSION, "ready": self.ready,
                 "session": self.session_id, "peer_uid": peer.uid, "pid": os.getpid(), "euid": os.geteuid()}
        if self._is_admin(peer):
            reply.update(backend=self.backend.name, backend_error=self.backend_error)
        elif self.backend_error:
            reply["backend_error"] = "unavailable"
        return reply

    async def _op_usage(self, req, peer, writer, fields):
        return self.usage()

    async def _op_policy(self, req, peer, writer, fields):
        return {"policy": self.policy.summary()}

    async def _resolve_image(self, req: dict) -> tuple[ImageSpec, str]:
        rules = self.policy.images
        setup = tuple(rules.setup_commands)
        has_image, has_ctx = "image" in req, "build_context_b64" in req
        if has_image == has_ctx:
            raise BadRequest("give exactly one of 'image' or 'build_context_b64'")
        if has_image:
            if not isinstance(req["image"], str):
                raise BadRequest("image must be a string")
            try:
                resolved = resolve_registry_image(rules, req["image"])
            except PermissionError as exc:
                raise PolicyDenied(str(exc)) from exc
            return ImageSpec("registry", pull_ref=resolved.pull_ref, setup_commands=setup), resolved.display
        data = _unb64(req["build_context_b64"], "build_context_b64")
        if len(data) > self.limits.max_context_bytes:
            raise PolicyDenied("build context exceeds the size limit")
        if not rules.build_contexts and not rules.allow_any_build_context:
            raise PolicyDenied("building images from a context is not enabled")
        root = self.policy.contexts_dir
        os.makedirs(root, mode=0o700, exist_ok=True)
        tmp = os.path.join(root, f".incoming-{uuid.uuid4().hex}")
        os.makedirs(tmp, mode=0o700)
        try:
            await asyncio.to_thread(safe_extract_context, data, tmp, self.limits.max_context_bytes,
                                    max_file_bytes=self.limits.max_context_file_bytes)
            digest = await asyncio.to_thread(hash_context_dir, tmp)
            if digest not in rules.build_contexts and not rules.allow_any_build_context:
                raise PolicyDenied(f"build context {digest} is not in the allowed list")
            final = os.path.join(root, digest)
            if os.path.isdir(final):
                shutil.rmtree(tmp, ignore_errors=True)
            else:
                os.replace(tmp, final)
        except BaseException:
            shutil.rmtree(tmp, ignore_errors=True)
            raise
        return (ImageSpec("context", context_dir=final, context_sha256=digest, setup_commands=setup),
                f"context:{digest}")

    async def _op_create(self, req, peer, writer, fields):
        if self.shutting_down:
            raise BrokerUnavailable("the broker is shutting down")
        L = self.limits
        image_spec, display = await self._resolve_image(req)
        fields["image"] = display
        cpu = _number(req, "cpu", L.default_cpu, L.min_cpu, L.max_cpu, float)
        if cpu != int(cpu) and not getattr(self.backend, "fractional_cpu", False):
            raise PolicyDenied(f"cpu={cpu}: this machine's sandbox platform allocates whole CPU cores only, so a "
                               "fractional cpu cannot be enforced exactly; ask for a whole number of cores")
        memory = _number(req, "memory_mb", L.default_memory_mb, L.min_memory_mb, L.max_memory_mb, int)
        timeout = _timeout(req, "timeout_s", L.default_timeout_s, L.max_timeout_s)
        idle = None
        if req.get("idle_timeout_s") is not None or L.idle_timeout_s:
            idle = _timeout(req, "idle_timeout_s", L.idle_timeout_s or L.max_idle_timeout_s, L.max_idle_timeout_s)
        workdir = _abs_path(req["workdir"], "workdir") if req.get("workdir") is not None else None
        env = _str_map(req.get("env"), "env", key_re=_ENV_KEY, max_items=256, max_value=32768)
        labels = _str_map(req.get("labels"), "labels", key_re=_LABEL_KEY, max_items=16, max_value=128)
        async with self._lock:
            if len(self.live()) + self.pending_creates >= L.max_concurrent:
                raise QuotaExceeded(f"concurrent sandbox limit reached ({L.max_concurrent})")
            if L.max_total_creates and self.creates_total >= L.max_total_creates:
                raise QuotaExceeded(f"sandbox creation limit reached ({L.max_total_creates})")
            remaining = self.budget_remaining()
            if remaining is not None:
                if remaining < L.min_create_budget_s:
                    raise QuotaExceeded("sandbox-seconds budget exhausted")
                timeout = int(min(timeout, remaining))
            self.pending_creates += 1
            self.creates_total += 1
        tags = {"sandbox-broker.session": self.session_id, "sandbox-broker.uid": str(peer.uid)}
        if self.parent_id:
            tags["sandbox-broker.parent"] = self.parent_id
        tags.update({f"label.{k}": v for k, v in labels.items()})
        hostname = self.policy.sandbox.hostname or None
        fallback = bool(hostname and not self.backend.native_hostname and self.policy.sandbox.normalize_prompt)
        env = {**RUNTIME_ENV, **env}  # an explicit client value wins
        if fallback:
            env = {**prompt_env(hostname), **env}
        spec = CreateSpec(image=image_spec, cpu=cpu, memory_mb=memory, timeout_s=timeout, idle_timeout_s=idle,
                          workdir=workdir, env=env or None, tags=tags, network=self.policy.sandbox.network,
                          hostname=hostname)
        fields.update(cpu=cpu, memory_mb=memory, timeout_s=timeout, idle_timeout_s=idle, network=self.network_label,
                      labels=labels or None)
        try:
            bid = await asyncio.wait_for(self.backend.create(spec), L.create_timeout_s)
        except BrokerError:
            raise
        except asyncio.TimeoutError as exc:
            raise self._fault("sandbox creation timed out", exc) from exc
        except ImageBuildError as exc:
            raise self._fault("sandbox creation failed: Image build failed", exc) from exc
        except Exception as exc:  # noqa: BLE001
            raise self._fault("sandbox creation failed", exc) from exc
        finally:
            async with self._lock:
                self.pending_creates -= 1
        now = self.clock()
        sid = "sbx-" + uuid.uuid4().hex[:16]
        rec = SandboxRecord(id=sid, owner_uid=peer.uid, image=display, cpu=cpu, memory_mb=memory,
                            timeout_s=timeout, idle_timeout_s=idle, created_at=now, deadline=now + timeout,
                            labels=labels, meta=self.backend.sandbox_meta(bid), backend_id=bid)
        self.records[sid] = rec
        self.peak_live = max(self.peak_live, len(self.live()))
        fields["sandbox_id"] = sid
        self.save_state()
        if fallback:
            await self._apply_hostname(rec, hostname)
        return {"id": sid, "sandbox": rec.public(now, self.network_label)}

    async def _apply_hostname(self, rec: SandboxRecord, hostname: str) -> None:
        async def sink(fd: str, chunk: bytes) -> None:
            return None

        try:
            await asyncio.wait_for(self.backend.exec(rec.backend_id, ["sh", "-c", HOSTNAME_FALLBACK, "_", hostname],
                                                     timeout_s=30, workdir=None, env=None, stdin=None,
                                                     on_output=sink), 60)
        except Exception as exc:  # noqa: BLE001 - best effort; the prompt env still applies
            log.info("hostname fallback on %s failed: %s", rec.id, exc)

    async def _op_exec(self, req, peer, writer, fields):
        rec = self._owned(req, peer)
        L = self.limits
        argv = req.get("argv")
        if (not isinstance(argv, list) or not argv or not all(isinstance(a, str) and "\0" not in a for a in argv)
                or sum(len(a) for a in argv) > 1 << 20):
            raise BadRequest("argv must be a non-empty list of strings (at most 1 MiB)")
        timeout = _timeout(req, "timeout_s", L.default_exec_timeout_s, L.max_exec_timeout_s)
        workdir = _abs_path(req["workdir"], "workdir") if req.get("workdir") is not None else None
        env = _str_map(req.get("env"), "env", key_re=_ENV_KEY, max_items=256, max_value=32768)
        stdin = _unb64(req["stdin_b64"], "stdin_b64") if req.get("stdin_b64") is not None else None
        if stdin is not None and len(stdin) > L.max_file_bytes:
            raise PolicyDenied("stdin exceeds the size limit")
        stream = bool(req.get("stream"))
        binary = bool(req.get("binary"))
        fields.update(sandbox_id=rec.id, argv=_short_argv(argv), timeout_s=timeout)

        cap = L.max_output_bytes
        bufs = {"stdout": bytearray(), "stderr": bytearray()}
        truncated = {"stdout": False, "stderr": False}
        decoders = {fd: codecs.getincrementaldecoder("utf-8")("replace") for fd in bufs}
        client_gone = False

        async def on_output(fd: str, chunk: bytes) -> None:
            nonlocal client_gone
            buf = bufs[fd]
            room = cap - len(buf)
            if room <= 0:
                truncated[fd] = True
                return
            if len(chunk) > room:
                chunk = chunk[:room]
                truncated[fd] = True
            buf.extend(chunk)
            if stream and writer is not None and not client_gone:
                ev: dict[str, Any] = {"event": "output", "fd": fd}
                if binary:
                    ev["data_b64"] = _b64(chunk)
                else:
                    ev["data"] = decoders[fd].decode(chunk)
                try:
                    writer.write(encode(ev))
                    await writer.drain()
                except (ConnectionError, BrokenPipeError):
                    client_gone = True

        t0 = time.monotonic()
        async with self._exec_sem:
            rec.execs += 1
            try:
                outcome = await asyncio.wait_for(
                    self.backend.exec(rec.backend_id, argv, timeout_s=timeout, workdir=workdir, env=env or None,
                                      stdin=stdin, on_output=on_output),
                    timeout + 60)
            except asyncio.TimeoutError as exc:
                raise self._fault(f"exec did not finish within {timeout + 60}s of its {timeout}s timeout; "
                                  "the sandbox may be unreachable", exc) from exc
            except KeyError as exc:
                raise SandboxNotFound(f"sandbox {rec.id!r} is not available") from exc
            except Exception as exc:  # noqa: BLE001
                raise self._fault("exec failed", exc) from exc
        result: dict[str, Any] = {
            "rc": outcome.returncode,
            "timed_out": outcome.timed_out,
            "stdout_truncated": truncated["stdout"],
            "stderr_truncated": truncated["stderr"],
            "duration_s": round(time.monotonic() - t0, 3),
        }
        if not stream:
            for fd, buf in bufs.items():
                if binary:
                    result[f"{fd}_b64"] = _b64(bytes(buf))
                else:
                    result[fd] = bytes(buf).decode("utf-8", "replace")
        fields.update(rc=outcome.returncode, timed_out=outcome.timed_out,
                      stdout_bytes=len(bufs["stdout"]), stderr_bytes=len(bufs["stderr"]))
        return result

    async def _op_put_file(self, req, peer, writer, fields):
        rec = self._owned(req, peer)
        path = _abs_path(req.get("path"), "path")
        data = _unb64(req.get("data_b64"), "data_b64")
        if len(data) > self.limits.max_file_bytes:
            raise PolicyDenied("file exceeds the size limit")
        mode = req.get("mode")
        if mode is not None and (isinstance(mode, bool) or not isinstance(mode, int) or not 0 <= mode <= 0o7777):
            raise BadRequest("mode must be an integer between 0 and 0o7777")
        fields.update(sandbox_id=rec.id, path=path, bytes=len(data))
        try:
            await self.backend.write_file(rec.backend_id, path, data, mode)
        except KeyError as exc:
            raise SandboxNotFound(f"sandbox {rec.id!r} is not available") from exc
        except Exception as exc:  # noqa: BLE001
            raise self._fault(f"write failed: {path}", exc) from exc
        return {"bytes": len(data)}

    async def _op_get_file(self, req, peer, writer, fields):
        rec = self._owned(req, peer)
        path = _abs_path(req.get("path"), "path")
        fields.update(sandbox_id=rec.id, path=path)
        try:
            data = await self.backend.read_file(rec.backend_id, path, self.limits.max_file_bytes)
        except FileTooLarge as exc:
            raise PolicyDenied("file exceeds the size limit") from exc
        except KeyError as exc:
            raise SandboxNotFound(f"sandbox {rec.id!r} is not available") from exc
        except FileNotFoundError as exc:
            raise BackendFailure(f"no such file: {path}") from exc
        except Exception as exc:  # noqa: BLE001
            raise self._fault(f"read failed: {path}", exc) from exc
        fields["bytes"] = len(data)
        return {"data_b64": _b64(data), "bytes": len(data)}

    async def _op_terminate(self, req, peer, writer, fields):
        rec = self._owned(req, peer, allow_ended=True)
        fields["sandbox_id"] = rec.id
        await self._terminate_rec(rec, "terminated")
        self.save_state()
        return {}

    async def _op_poll(self, req, peer, writer, fields):
        rec = self._owned(req, peer, allow_ended=True)
        if rec.ended_at is None and self.ready:
            try:
                rc = await self.backend.poll(rec.backend_id)
            except Exception as exc:  # noqa: BLE001
                raise self._fault("poll failed", exc) from exc
            if rc is not None:
                self._end(rec, "exited", rc)
                await self._flush_forgets()
        return {"running": rec.ended_at is None, "rc": rec.returncode, "end_reason": rec.end_reason}

    async def _op_list(self, req, peer, writer, fields):
        now = self.clock()
        everyone = bool(req.get("all")) and peer.uid in self.policy.admin_uids
        recs = [r for r in self.records.values() if everyone or r.owner_uid == peer.uid]
        return {"sandboxes": [r.public(now, self.network_label) for r in recs]}

    async def _op_shutdown(self, req, peer, writer, fields):
        summary = await self.shutdown("request")
        if req.get("exit", True):
            asyncio.get_running_loop().call_later(0.2, self._stop.set)
        return {"summary": summary}

    # ------------------------------------------------------------------ lifecycle

    async def shutdown(self, reason: str) -> dict[str, Any]:
        if not self.shutting_down:
            self.shutting_down = True
            live = self.live()
            await asyncio.gather(*(self._terminate_rec(r, "shutdown") for r in live), return_exceptions=True)
            self.audit.write("shutdown", reason=reason, terminated=len(live), summary=self.usage(), sync=True)
            self.save_state()
        return self.usage()

    async def reap_once(self, *, poll: bool) -> None:
        now = self.clock()
        for rec in self.live():
            if now >= rec.deadline + 15:
                await self._terminate_rec(rec, "timeout")
        budget = self.limits.budget_sandbox_seconds
        if budget and self.used_seconds(now) >= budget and self.live():
            if not self.budget_exhausted:
                self.budget_exhausted = True
                self.audit.write("budget_exhausted", used_sandbox_seconds=round(self.used_seconds(now), 1),
                                 budget_sandbox_seconds=budget, sync=True)
            await asyncio.gather(*(self._terminate_rec(r, "budget") for r in self.live()), return_exceptions=True)
        if poll and self.ready:
            sem = asyncio.Semaphore(16)

            async def check(rec: SandboxRecord) -> None:
                async with sem:
                    try:
                        rc = await asyncio.wait_for(self.backend.poll(rec.backend_id), 60)
                    except Exception as exc:  # noqa: BLE001
                        log.debug("poll %s failed: %s", rec.id, exc)
                        return
                    if rc is not None:
                        self._end(rec, "exited", rc)

            await asyncio.gather(*(check(r) for r in self.live()))
        await self._flush_forgets()
        if self.ready and now - self._last_maintain >= float(getattr(self.backend, "maintain_interval_s", 60.0)):
            self._last_maintain = now
            try:
                await self.backend.maintain()
            except Exception as exc:  # noqa: BLE001
                log.warning("backend maintenance failed: %s", exc)
        if now - self._last_usage_log >= self.limits.usage_log_interval_s:
            self._last_usage_log = now
            self.audit.write("usage", **self.usage())
        self.save_state()

    async def _reaper(self) -> None:
        last_poll = time.monotonic()
        while not self._stop.is_set():
            try:
                await asyncio.wait_for(self._stop.wait(), self.limits.reap_interval_s)
                return
            except asyncio.TimeoutError:
                pass
            do_poll = time.monotonic() - last_poll >= self.limits.poll_interval_s
            if do_poll:
                last_poll = time.monotonic()
            try:
                await self.reap_once(poll=do_poll)
            except Exception:  # noqa: BLE001
                log.exception("reaper pass failed")

    async def start_backend(self, attempts: int = 10, delay_s: float = 15.0) -> None:
        for attempt in range(1, attempts + 1):
            try:
                await self.backend.start()
                await self.load_state()
                self.ready = True
                self.backend_error = None
                log.info("backend %s ready (attempt %d)", self.backend.name, attempt)
                self.audit.write("backend_ready", attempt=attempt, sync=True)
                return
            except Exception as exc:  # noqa: BLE001
                self.backend_error = f"{type(exc).__name__}: {exc}"
                log.warning("backend start failed (attempt %d): %s", attempt, self.backend_error)
                self.audit.write("backend_error", error="backend unavailable", attempt=attempt, sync=True)
                if attempt < attempts:
                    await asyncio.sleep(delay_s)

    def _bind(self) -> socket.socket:
        path = self.policy.socket_path
        if os.path.lexists(path):
            st = os.lstat(path)
            if not stat.S_ISSOCK(st.st_mode):
                raise RuntimeError(f"{path} exists and is not a socket")
            probe = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                probe.connect(path)
                raise RuntimeError(f"another gate daemon is already listening on {path}")
            except (ConnectionRefusedError, FileNotFoundError):
                os.unlink(path)
            finally:
                probe.close()
        os.makedirs(os.path.dirname(path) or "/", exist_ok=True)
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        old = os.umask(0o177)
        try:
            sock.bind(path)
        finally:
            os.umask(old)
        if self.policy.socket_group:
            import grp

            os.chown(path, 0 if os.geteuid() == 0 else -1, grp.getgrnam(self.policy.socket_group).gr_gid)
        os.chmod(path, self.policy.socket_mode)
        sock.listen(256)
        return sock

    async def serve(self) -> None:
        """Run until shutdown or a termination signal."""
        loop = asyncio.get_running_loop()
        os.makedirs(self.policy.state_dir, mode=0o700, exist_ok=True)
        os.chmod(self.policy.state_dir, 0o700)
        log.info("starting with backend %s (parent %s)", self.backend.name, self.parent_id or "-")
        self.audit.write("start", version=__version__, pid=os.getpid(), policy_sha256=self.policy.source_sha256,
                         policy=self.policy.summary(), sync=True)
        sock = self._bind()
        line_limit = max(self.limits.max_file_bytes, self.limits.max_context_bytes) * 4 // 3 + (1 << 20)
        self._server = await asyncio.start_unix_server(self.handle_connection, sock=sock, limit=line_limit)
        self._tasks.append(asyncio.create_task(self.start_backend()))
        self._tasks.append(asyncio.create_task(self._reaper()))
        for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
            try:
                loop.add_signal_handler(sig, lambda s=sig: asyncio.ensure_future(self._on_signal(s)))
            except (NotImplementedError, RuntimeError):
                pass
        try:
            await self._stop.wait()
        finally:
            self._server.close()
            for t in self._tasks:
                t.cancel()
            await asyncio.gather(*self._tasks, return_exceptions=True)
            if not self.shutting_down:
                await self.shutdown("exit")
            try:
                os.unlink(self.policy.socket_path)
            except OSError:
                pass
            await self.backend.close()
            self.audit.write("stopped", sync=True)
            self.audit.close()

    async def _on_signal(self, sig: int) -> None:
        await self.shutdown(f"signal {signal.Signals(sig).name}")
        self._stop.set()

    def request_stop(self) -> None:
        self._stop.set()
