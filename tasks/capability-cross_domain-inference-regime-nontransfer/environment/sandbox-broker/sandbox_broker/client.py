"""Clients for the sandbox gate (standard library only, platform-neutral).

Sync::

    from sandbox_broker import BrokerClient
    client = BrokerClient()
    sb = client.create("python:3.12-slim-bookworm", cpu=1, memory_mb=2048, timeout_s=1800)
    r = sb.exec("bash", "-c", "ls /app", timeout=60)
    print(r.returncode, r.stdout)
    sb.put_file("/tmp/x.txt", b"hello")
    sb.terminate()

Async: the same names on ``AsyncBrokerClient`` / ``AsyncSandbox``, awaited.
"""
from __future__ import annotations

import asyncio
import base64
import dataclasses
import io
import json
import os
import socket
import tarfile
import uuid
from pathlib import Path
from typing import Any, Awaitable, Callable

from .policy import DEFAULT_SOCKET_PATH
from .protocol import BrokerUnavailable, encode, error_from_reply

OutputHandler = Callable[[str, "str | bytes"], Any]

CREATE_REPLY_TIMEOUT = 1800.0
EXEC_GRACE = 120.0
FILE_REPLY_TIMEOUT = 600.0


def default_socket_path() -> str:
    return os.environ.get("SANDBOX_GATE_SOCKET") or os.environ.get("SANDBOX_BROKER_SOCKET") or DEFAULT_SOCKET_PATH


@dataclasses.dataclass
class ExecResult:
    returncode: int
    stdout: str | bytes
    stderr: str | bytes
    timed_out: bool = False
    stdout_truncated: bool = False
    stderr_truncated: bool = False
    duration_s: float = 0.0

    @property
    def exit_code(self) -> int:
        return self.returncode

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def _create_msg(image, build_context, cpu, memory_mb, timeout_s, idle_timeout_s, workdir, env, labels):
    msg: dict[str, Any] = {"op": "create"}
    if (image is None) == (build_context is None):
        raise ValueError("give exactly one of image or build_context")
    if image is not None:
        msg["image"] = image
    else:
        msg["build_context_b64"] = base64.b64encode(pack_build_context(build_context)).decode()
    for key, val in (("cpu", cpu), ("memory_mb", memory_mb), ("timeout_s", timeout_s),
                     ("idle_timeout_s", idle_timeout_s), ("workdir", workdir), ("env", env), ("labels", labels)):
        if val is not None:
            msg[key] = val
    return msg


def _exec_reply_timeout(timeout):
    # No timeout given: the daemon applies the policy default/max, so wait for its reply without a client-side cap.
    return None if timeout is None else timeout + EXEC_GRACE


def _exec_msg(sid, argv, timeout, workdir, env, stdin, binary, stream):
    if len(argv) == 1 and isinstance(argv[0], (list, tuple)):
        argv = tuple(argv[0])
    msg: dict[str, Any] = {"op": "exec", "id": sid, "argv": [str(a) for a in argv]}
    if timeout is not None:
        msg["timeout_s"] = int(timeout)
    if workdir is not None:
        msg["workdir"] = workdir
    if env:
        msg["env"] = {k: str(v) for k, v in env.items() if v is not None}
    if stdin is not None:
        data = stdin.encode() if isinstance(stdin, str) else bytes(stdin)
        msg["stdin_b64"] = base64.b64encode(data).decode()
    if binary:
        msg["binary"] = True
    if stream:
        msg["stream"] = True
    return msg


def _exec_result(reply: dict, binary: bool, streamed: dict[str, list] | None) -> ExecResult:
    if streamed is not None:
        if binary:
            out, err = b"".join(streamed["stdout"]), b"".join(streamed["stderr"])
        else:
            out, err = "".join(streamed["stdout"]), "".join(streamed["stderr"])
    elif binary:
        out = base64.b64decode(reply.get("stdout_b64", ""))
        err = base64.b64decode(reply.get("stderr_b64", ""))
    else:
        out, err = reply.get("stdout", ""), reply.get("stderr", "")
    return ExecResult(returncode=int(reply.get("rc", -1)), stdout=out, stderr=err,
                      timed_out=bool(reply.get("timed_out")), stdout_truncated=bool(reply.get("stdout_truncated")),
                      stderr_truncated=bool(reply.get("stderr_truncated")),
                      duration_s=float(reply.get("duration_s", 0.0)))


def _event_data(ev: dict, binary: bool):
    return base64.b64decode(ev.get("data_b64", "")) if binary else ev.get("data", "")


def pack_build_context(path: str | os.PathLike | bytes) -> bytes:
    """tar.gz of a Docker build context directory (the Dockerfile must be at its root)."""
    if isinstance(path, (bytes, bytearray)):
        return bytes(path)
    root = Path(path)
    if not (root / "Dockerfile").is_file():
        raise ValueError(f"{root} has no Dockerfile")
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        for p in sorted(root.rglob("*")):
            if p.is_symlink():
                raise ValueError(f"symlinks are not supported in build contexts: {p}")
            rel = p.relative_to(root).as_posix()
            info = tf.gettarinfo(str(p), arcname=rel)
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mtime = 0
            if p.is_file():
                with open(p, "rb") as f:
                    tf.addfile(info, f)
            elif p.is_dir():
                tf.addfile(info)
    return buf.getvalue()


def _tar_dir(local_dir: str | os.PathLike) -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        tf.add(str(local_dir), arcname=".")
    return buf.getvalue()


def _untar(data: bytes, dest: str | os.PathLike) -> None:
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as tf:
        try:
            tf.extractall(dest, filter="data")
        except TypeError:  # Python < 3.12 without extraction filters
            for m in tf.getmembers():
                target = (dest / m.name).resolve()
                if not str(target).startswith(str(dest.resolve())) or m.issym() or m.islnk() or m.isdev():
                    continue
                tf.extract(m, dest)


# ============================================================================ sync


class BrokerClient:
    def __init__(self, socket_path: str | None = None, connect_timeout: float = 30.0):
        self.socket_path = socket_path or default_socket_path()
        self.connect_timeout = connect_timeout

    def _connect(self) -> socket.socket:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(self.connect_timeout)
        try:
            s.connect(self.socket_path)
        except (FileNotFoundError, ConnectionRefusedError) as exc:
            s.close()
            raise BrokerUnavailable(f"sandbox broker is not running at {self.socket_path}") from exc
        return s

    def call(self, msg: dict, timeout: float | None = 300.0,
             on_event: Callable[[dict], None] | None = None) -> dict:
        s = self._connect()
        try:
            s.settimeout(timeout)
            s.sendall(encode(msg))
            f = s.makefile("rb")
            while True:
                line = f.readline()
                if not line:
                    raise BrokerUnavailable(f"broker closed the connection during {msg.get('op')}")
                reply = json.loads(line)
                if "event" in reply:
                    if on_event:
                        on_event(reply)
                    continue
                if not reply.get("ok", "error" not in reply):
                    raise error_from_reply(reply)
                return reply
        except socket.timeout as exc:
            raise TimeoutError(f"no reply from broker for {msg.get('op')} within {timeout}s") from exc
        finally:
            s.close()

    def ping(self, timeout: float = 10.0) -> dict:
        return self.call({"op": "ping"}, timeout=timeout)

    def usage(self) -> dict:
        return self.call({"op": "usage"})

    def policy(self) -> dict:
        return self.call({"op": "policy"})["policy"]

    def list(self, all: bool = False) -> list[dict]:
        return self.call({"op": "list", **({"all": True} if all else {})})["sandboxes"]

    def shutdown(self, exit: bool = True) -> dict:
        return self.call({"op": "shutdown", "exit": exit}, timeout=600)["summary"]

    def create(self, image: str | None = None, *, build_context: str | os.PathLike | bytes | None = None,
               cpu: float | None = None, memory_mb: int | None = None, timeout_s: int | None = None,
               idle_timeout_s: int | None = None, workdir: str | None = None, env: dict | None = None,
               labels: dict | None = None) -> "Sandbox":
        msg = _create_msg(image, build_context, cpu, memory_mb, timeout_s, idle_timeout_s, workdir, env, labels)
        reply = self.call(msg, timeout=CREATE_REPLY_TIMEOUT)
        return Sandbox(self, reply["id"], reply.get("sandbox", {}))

    def sandbox(self, sandbox_id: str) -> "Sandbox":
        return Sandbox(self, sandbox_id, {})


class Sandbox:
    def __init__(self, client: BrokerClient, sandbox_id: str, info: dict):
        self.client = client
        self.id = sandbox_id
        self.info = info

    @property
    def object_id(self) -> str:
        return self.id

    def exec(self, *argv: str, timeout: int | None = None, workdir: str | None = None, env: dict | None = None,
             stdin: str | bytes | None = None, binary: bool = False,
             on_output: OutputHandler | None = None) -> ExecResult:
        stream = on_output is not None
        msg = _exec_msg(self.id, argv, timeout, workdir, env, stdin, binary, stream)
        streamed: dict[str, list] | None = {"stdout": [], "stderr": []} if stream else None

        def on_event(ev: dict) -> None:
            data = _event_data(ev, binary)
            streamed[ev["fd"]].append(data)
            on_output(ev["fd"], data)

        reply = self.client.call(msg, timeout=_exec_reply_timeout(timeout), on_event=on_event if stream else None)
        return _exec_result(reply, binary, streamed)

    run = exec

    def put_file(self, path: str, data: str | bytes | os.PathLike, mode: int | None = None) -> None:
        if isinstance(data, os.PathLike):
            data = Path(data).read_bytes()
        elif isinstance(data, str):
            data = data.encode()
        msg = {"op": "put_file", "id": self.id, "path": path, "data_b64": base64.b64encode(data).decode()}
        if mode is not None:
            msg["mode"] = mode
        self.client.call(msg, timeout=FILE_REPLY_TIMEOUT)

    def get_file(self, path: str) -> bytes:
        reply = self.client.call({"op": "get_file", "id": self.id, "path": path}, timeout=FILE_REPLY_TIMEOUT)
        return base64.b64decode(reply["data_b64"])

    def upload_dir(self, local_dir: str | os.PathLike, remote_dir: str) -> None:
        tmp = f"/tmp/.sandbox-broker-{uuid.uuid4().hex}.tar.gz"
        self.put_file(tmp, _tar_dir(local_dir))
        r = self.exec("sh", "-c", 'mkdir -p "$1" && tar -xzf "$2" -C "$1"; rc=$?; rm -f "$2"; exit $rc',
                      "_", remote_dir, tmp, timeout=600)
        if r.returncode != 0:
            raise RuntimeError(f"upload_dir failed ({r.returncode}): {r.stderr}")

    def download_dir(self, remote_dir: str, local_dir: str | os.PathLike) -> None:
        tmp = f"/tmp/.sandbox-broker-{uuid.uuid4().hex}.tar.gz"
        r = self.exec("tar", "-czf", tmp, "-C", remote_dir, ".", timeout=600)
        if r.returncode != 0:
            raise RuntimeError(f"download_dir failed ({r.returncode}): {r.stderr}")
        try:
            _untar(self.get_file(tmp), local_dir)
        finally:
            self.exec("rm", "-f", tmp, timeout=60)

    def poll(self) -> int | None:
        reply = self.client.call({"op": "poll", "id": self.id})
        return None if reply["running"] else (reply.get("rc") if reply.get("rc") is not None else 0)

    def terminate(self) -> None:
        self.client.call({"op": "terminate", "id": self.id}, timeout=180)

    def __enter__(self) -> "Sandbox":
        return self

    def __exit__(self, *exc) -> None:
        try:
            self.terminate()
        except Exception:  # noqa: BLE001
            pass


# ============================================================================ async


class AsyncBrokerClient:
    def __init__(self, socket_path: str | None = None, connect_timeout: float = 30.0):
        self.socket_path = socket_path or default_socket_path()
        self.connect_timeout = connect_timeout

    async def call(self, msg: dict, timeout: float | None = 300.0,
                   on_event: Callable[[dict], Awaitable[None] | None] | None = None) -> dict:
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_unix_connection(self.socket_path, limit=1 << 30), self.connect_timeout)
        except (FileNotFoundError, ConnectionRefusedError) as exc:
            raise BrokerUnavailable(f"sandbox broker is not running at {self.socket_path}") from exc
        try:
            writer.write(encode(msg))
            await writer.drain()

            async def read_reply() -> dict:
                while True:
                    line = await reader.readline()
                    if not line:
                        raise BrokerUnavailable(f"broker closed the connection during {msg.get('op')}")
                    reply = json.loads(line)
                    if "event" in reply:
                        if on_event:
                            res = on_event(reply)
                            if asyncio.iscoroutine(res):
                                await res
                        continue
                    return reply

            try:
                reply = await asyncio.wait_for(read_reply(), timeout)
            except asyncio.TimeoutError as exc:
                raise TimeoutError(f"no reply from broker for {msg.get('op')} within {timeout}s") from exc
        finally:
            writer.close()
        if not reply.get("ok", "error" not in reply):
            raise error_from_reply(reply)
        return reply

    async def ping(self, timeout: float = 10.0) -> dict:
        return await self.call({"op": "ping"}, timeout=timeout)

    async def usage(self) -> dict:
        return await self.call({"op": "usage"})

    async def policy(self) -> dict:
        return (await self.call({"op": "policy"}))["policy"]

    async def list(self, all: bool = False) -> list[dict]:
        return (await self.call({"op": "list", **({"all": True} if all else {})}))["sandboxes"]

    async def shutdown(self, exit: bool = True) -> dict:
        return (await self.call({"op": "shutdown", "exit": exit}, timeout=600))["summary"]

    async def create(self, image: str | None = None, *, build_context: str | os.PathLike | bytes | None = None,
                     cpu: float | None = None, memory_mb: int | None = None, timeout_s: int | None = None,
                     idle_timeout_s: int | None = None, workdir: str | None = None, env: dict | None = None,
                     labels: dict | None = None) -> "AsyncSandbox":
        if build_context is not None and not isinstance(build_context, (bytes, bytearray)):
            build_context = await asyncio.to_thread(pack_build_context, build_context)
        msg = _create_msg(image, build_context, cpu, memory_mb, timeout_s, idle_timeout_s, workdir, env, labels)
        reply = await self.call(msg, timeout=CREATE_REPLY_TIMEOUT)
        return AsyncSandbox(self, reply["id"], reply.get("sandbox", {}))

    def sandbox(self, sandbox_id: str) -> "AsyncSandbox":
        return AsyncSandbox(self, sandbox_id, {})


class AsyncSandbox:
    def __init__(self, client: AsyncBrokerClient, sandbox_id: str, info: dict):
        self.client = client
        self.id = sandbox_id
        self.info = info

    @property
    def object_id(self) -> str:
        return self.id

    async def exec(self, *argv: str, timeout: int | None = None, workdir: str | None = None,
                   env: dict | None = None, stdin: str | bytes | None = None, binary: bool = False,
                   on_output: OutputHandler | None = None) -> ExecResult:
        stream = on_output is not None
        msg = _exec_msg(self.id, argv, timeout, workdir, env, stdin, binary, stream)
        streamed: dict[str, list] | None = {"stdout": [], "stderr": []} if stream else None

        async def on_event(ev: dict) -> None:
            data = _event_data(ev, binary)
            streamed[ev["fd"]].append(data)
            res = on_output(ev["fd"], data)
            if asyncio.iscoroutine(res):
                await res

        reply = await self.client.call(msg, timeout=_exec_reply_timeout(timeout),
                                       on_event=on_event if stream else None)
        return _exec_result(reply, binary, streamed)

    run = exec

    async def put_file(self, path: str, data: str | bytes | os.PathLike, mode: int | None = None) -> None:
        if isinstance(data, os.PathLike):
            data = await asyncio.to_thread(Path(data).read_bytes)
        elif isinstance(data, str):
            data = data.encode()
        msg = {"op": "put_file", "id": self.id, "path": path, "data_b64": base64.b64encode(data).decode()}
        if mode is not None:
            msg["mode"] = mode
        await self.client.call(msg, timeout=FILE_REPLY_TIMEOUT)

    async def get_file(self, path: str) -> bytes:
        reply = await self.client.call({"op": "get_file", "id": self.id, "path": path}, timeout=FILE_REPLY_TIMEOUT)
        return base64.b64decode(reply["data_b64"])

    async def upload_dir(self, local_dir: str | os.PathLike, remote_dir: str) -> None:
        tmp = f"/tmp/.sandbox-broker-{uuid.uuid4().hex}.tar.gz"
        await self.put_file(tmp, await asyncio.to_thread(_tar_dir, local_dir))
        r = await self.exec("sh", "-c", 'mkdir -p "$1" && tar -xzf "$2" -C "$1"; rc=$?; rm -f "$2"; exit $rc',
                            "_", remote_dir, tmp, timeout=600)
        if r.returncode != 0:
            raise RuntimeError(f"upload_dir failed ({r.returncode}): {r.stderr}")

    async def download_dir(self, remote_dir: str, local_dir: str | os.PathLike) -> None:
        tmp = f"/tmp/.sandbox-broker-{uuid.uuid4().hex}.tar.gz"
        r = await self.exec("tar", "-czf", tmp, "-C", remote_dir, ".", timeout=600)
        if r.returncode != 0:
            raise RuntimeError(f"download_dir failed ({r.returncode}): {r.stderr}")
        try:
            await asyncio.to_thread(_untar, await self.get_file(tmp), local_dir)
        finally:
            await self.exec("rm", "-f", tmp, timeout=60)

    async def poll(self) -> int | None:
        reply = await self.client.call({"op": "poll", "id": self.id})
        return None if reply["running"] else (reply.get("rc") if reply.get("rc") is not None else 0)

    async def terminate(self) -> None:
        await self.client.call({"op": "terminate", "id": self.id}, timeout=180)

    async def __aenter__(self) -> "AsyncSandbox":
        return self

    async def __aexit__(self, *exc) -> None:
        try:
            await self.terminate()
        except Exception:  # noqa: BLE001
            pass


__all__ = ["AsyncBrokerClient", "AsyncSandbox", "BrokerClient", "ExecResult", "Sandbox",
                          "default_socket_path", "pack_build_context"]
