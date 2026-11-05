from __future__ import annotations
import asyncio
import os
import shutil
import tempfile
import time
import uuid
from typing import Any, Mapping
from .base import NETWORK_EGRESS, NETWORK_NONE, Backend, CreateSpec, ExecOutcome, FileTooLarge, OutputCallback
class _Box:
    def __init__(self, root: str, spec: CreateSpec):
        self.root = root
        self.spec = spec
        self.created = time.time()
        self.returncode: int | None = None
class LocalBackend(Backend):
    name = "local"
    network_modes = (NETWORK_NONE, NETWORK_EGRESS)
    @classmethod
    def from_config(cls, settings: Mapping[str, Any], credentials: Mapping[str, Any], *,
                    state_dir: str) -> "LocalBackend":
        return cls(os.path.join(state_dir, "local"))
    def __init__(self, base_dir: str | None = None, create_delay_s: float = 0.0, map_paths: bool = True):
        self.base_dir = base_dir or tempfile.mkdtemp(prefix="sandbox-broker-local-")
        self.map_paths = map_paths
        self.create_delay_s = create_delay_s
        self.boxes: dict[str, _Box] = {}
        self.created_specs: list[CreateSpec] = []
        self.terminated: list[str] = []
        self.fail_next_create: Exception | None = None
    def _box(self, sid: str) -> _Box:
        box = self.boxes.get(sid)
        if box is None or box.returncode is not None:
            raise KeyError(sid)
        return box
    def _path(self, box: _Box, path: str) -> str:
        return os.path.join(box.root, path.lstrip("/")) if self.map_paths else path
    async def create(self, spec: CreateSpec) -> str:
        if self.fail_next_create is not None:
            exc, self.fail_next_create = self.fail_next_create, None
            raise exc
        if self.create_delay_s:
            await asyncio.sleep(self.create_delay_s)
        sid = "lb-" + uuid.uuid4().hex[:16]
        root = os.path.join(self.base_dir, sid)
        os.makedirs(root)
        self.boxes[sid] = _Box(root, spec)
        self.created_specs.append(spec)
        return sid
    async def attach(self, sandbox_id: str, meta: dict | None = None) -> bool:
        return sandbox_id in self.boxes and self.boxes[sandbox_id].returncode is None
    async def exec(self, sandbox_id, argv, *, timeout_s, workdir, env, stdin, on_output: OutputCallback):
        box = self._box(sandbox_id)
        cwd = self._path(box, workdir) if workdir else box.root
        os.makedirs(cwd, exist_ok=True)
        full_env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "SANDBOX_ROOT": box.root,
                    **(box.spec.env or {}), **(env or {})}
        proc = await asyncio.create_subprocess_exec(
            *argv, cwd=cwd, env=full_env, stdin=asyncio.subprocess.PIPE if stdin is not None else asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, start_new_session=True)
        async def pump(stream, fd):
            while True:
                chunk = await stream.read(65536)
                if not chunk:
                    return
                await on_output(fd, chunk)
        async def feed():
            if stdin is not None:
                proc.stdin.write(stdin)
                await proc.stdin.drain()
                proc.stdin.close()
        work = asyncio.gather(feed(), pump(proc.stdout, "stdout"), pump(proc.stderr, "stderr"), proc.wait())
        try:
            await asyncio.wait_for(work, timeout_s)
        except asyncio.TimeoutError:
            try:
                os.killpg(proc.pid, 9)
            except ProcessLookupError:
                pass
            await proc.wait()
            return ExecOutcome(returncode=-1, timed_out=True)
        return ExecOutcome(returncode=proc.returncode)
    async def write_file(self, sandbox_id, path, data, mode):
        box = self._box(sandbox_id)
        p = self._path(box, path)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(data)
        if mode is not None:
            os.chmod(p, mode)
    async def read_file(self, sandbox_id, path, max_bytes):
        box = self._box(sandbox_id)
        p = self._path(box, path)
        if os.path.getsize(p) > max_bytes:
            raise FileTooLarge(path)
        with open(p, "rb") as f:
            return f.read()
    async def terminate(self, sandbox_id):
        box = self.boxes.get(sandbox_id)
        if box is None:
            return
        if box.returncode is None:
            box.returncode = 137
            self.terminated.append(sandbox_id)
            shutil.rmtree(box.root, ignore_errors=True)
    async def poll(self, sandbox_id):
        box = self.boxes.get(sandbox_id)
        if box is None:
            return 137
        if box.returncode is None and time.time() > box.created + box.spec.timeout_s:
            box.returncode = 0
        return box.returncode
    def expire(self, sandbox_id: str, returncode: int = 0) -> None:
        self.boxes[sandbox_id].returncode = returncode
    def live_ids(self) -> list[str]:
        return [sid for sid, b in self.boxes.items() if b.returncode is None]
