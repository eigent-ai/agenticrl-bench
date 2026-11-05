from __future__ import annotations
import abc
import dataclasses
from typing import Any, Awaitable, Callable, Mapping
OutputCallback = Callable[[str, bytes], Awaitable[None]]
NETWORK_NONE = "none"
NETWORK_EGRESS = "egress"
NETWORK_MODES = (NETWORK_NONE, NETWORK_EGRESS)
@dataclasses.dataclass(frozen=True)
class ImageSpec:
    kind: str
    pull_ref: str | None = None
    context_dir: str | None = None
    context_sha256: str | None = None
    setup_commands: tuple[str, ...] = ()
    @property
    def cache_key(self) -> tuple:
        return (self.kind, self.pull_ref, self.context_sha256, self.setup_commands)
@dataclasses.dataclass(frozen=True)
class CreateSpec:
    image: ImageSpec
    cpu: float
    memory_mb: int
    timeout_s: int
    idle_timeout_s: int | None
    workdir: str | None = None
    env: dict[str, str] | None = None
    tags: dict[str, str] | None = None
    network: str = NETWORK_NONE
    hostname: str | None = None
@dataclasses.dataclass
class ExecOutcome:
    returncode: int
    timed_out: bool = False
class FileTooLarge(Exception):
    pass
class ImageBuildError(Exception):
    pass
class Backend(abc.ABC):
    name = "base"
    native_hostname = False
    network_modes: tuple[str, ...] = (NETWORK_NONE,)
    @classmethod
    def from_config(cls, settings: Mapping[str, Any], credentials: Mapping[str, Any], *, state_dir: str) -> "Backend":
        return cls()
    @classmethod
    def capture_runtime(cls, env: Mapping[str, str]) -> dict[str, str]:
        return {}
    async def start(self) -> None:
        pass
    async def close(self) -> None:
        pass
    async def maintain(self) -> None:
        pass
    @abc.abstractmethod
    async def create(self, spec: CreateSpec) -> str:
        pass
    async def attach(self, sandbox_id: str, meta: dict | None = None) -> bool:
        return False
    def sandbox_meta(self, sandbox_id: str) -> dict:
        return {}
    async def forget(self, sandbox_id: str) -> None:
        pass
    @abc.abstractmethod
    async def exec(self, sandbox_id: str, argv: list[str], *, timeout_s: int, workdir: str | None,
                   env: dict[str, str] | None, stdin: bytes | None,
                   on_output: OutputCallback) -> ExecOutcome:
        pass
    @abc.abstractmethod
    async def write_file(self, sandbox_id: str, path: str, data: bytes, mode: int | None) -> None:
        pass
    @abc.abstractmethod
    async def read_file(self, sandbox_id: str, path: str, max_bytes: int) -> bytes:
        pass
    @abc.abstractmethod
    async def terminate(self, sandbox_id: str) -> None:
        pass
    @abc.abstractmethod
    async def poll(self, sandbox_id: str) -> int | None:
        pass
