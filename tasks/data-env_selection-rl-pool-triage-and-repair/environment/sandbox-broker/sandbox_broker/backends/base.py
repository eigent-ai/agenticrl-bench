"""Backend contract: what a sandbox platform must provide to the gate (see BACKENDS.md).

Everything above this interface (protocol, policy, quotas, audit, CLI, Harbor plugin) is
platform-neutral. A backend is the only place that knows the platform: its SDK, its object
ids, its network model and its error types. Nothing a backend returns is shown to
non-admin clients except through the neutral fields defined here.
"""
from __future__ import annotations

import abc
import dataclasses
from typing import Any, Awaitable, Callable, Mapping

OutputCallback = Callable[[str, bytes], Awaitable[None]]  # (fd name "stdout" | "stderr", chunk)

NETWORK_NONE = "none"  # no outbound network at all (the default and the only value agents ever get)
NETWORK_EGRESS = "egress"  # unrestricted outbound network (operator-only, e.g. a verifier battery)
NETWORK_MODES = (NETWORK_NONE, NETWORK_EGRESS)


@dataclasses.dataclass(frozen=True)
class ImageSpec:
    kind: str  # "registry" | "context"
    pull_ref: str | None = None
    context_dir: str | None = None  # a directory with a Dockerfile at its root (already allow-listed)
    context_sha256: str | None = None
    setup_commands: tuple[str, ...] = ()  # run as root after the image is built, as extra image layers

    @property
    def cache_key(self) -> tuple:
        return (self.kind, self.pull_ref, self.context_sha256, self.setup_commands)


@dataclasses.dataclass(frozen=True)
class CreateSpec:
    image: ImageSpec
    cpu: float  # cores, request == limit
    memory_mb: int  # MiB, request == limit
    timeout_s: int  # hard lifetime
    idle_timeout_s: int | None
    workdir: str | None = None
    env: dict[str, str] | None = None  # environment of every process in the sandbox
    tags: dict[str, str] | None = None  # platform-side metadata (never shown to the workload)
    network: str = NETWORK_NONE  # one of NETWORK_MODES
    hostname: str | None = None  # what gethostname() should return inside the sandbox; None = platform default


@dataclasses.dataclass
class ExecOutcome:
    returncode: int  # -1 when the command was killed for its timeout
    timed_out: bool = False


class FileTooLarge(Exception):
    """read_file: the file is larger than ``max_bytes``."""


class ImageBuildError(Exception):
    """create: the image could not be built or pulled (a problem with the image, not the platform).

    The gate reports it to clients as ``image_build`` with the text "Image build failed", so
    callers can tell a broken task image from a platform fault.
    """


class Backend(abc.ABC):
    """Creates and drives sandboxes on one platform.

    Required guarantees (the gate relies on them; see BACKENDS.md):
      * ``create`` honours ``spec.network``: with ``NETWORK_NONE`` the sandbox has no outbound
        network of any kind. A backend that cannot guarantee this must raise from ``create``.
      * cpu / memory / timeout_s / idle_timeout_s are enforced by the platform.
      * sandbox ids returned by ``create`` are opaque to the gate; clients never see them.
    """

    #: registry name, used in the root-only backend config (``provider = "<name>"``)
    name = "base"
    #: True when ``create`` sets the hostname natively from ``spec.hostname``; otherwise the
    #: gate applies its best-effort fallback (see server.HOSTNAME_FALLBACK)
    native_hostname = False
    #: network modes this backend can create
    network_modes: tuple[str, ...] = (NETWORK_NONE,)

    # ------------------------------------------------------------------ construction

    @classmethod
    def from_config(cls, settings: Mapping[str, Any], credentials: Mapping[str, Any], *, state_dir: str) -> "Backend":
        """Build the backend from its ``[provider]`` settings and the credentials record.

        ``credentials`` is the record written by ``capture_credentials`` (or read from the
        operator's credentials file); the caller clears it afterwards.
        """
        return cls()  # type: ignore[call-arg]

    @classmethod
    def capture_runtime(cls, env: Mapping[str, str]) -> dict[str, str]:
        """Platform facts about the machine the daemon runs on, read from the root ``start``
        environment and kept in the root-only credentials record (e.g. this container's own id)."""
        return {}

    # ------------------------------------------------------------------ lifecycle

    async def start(self) -> None:
        """Connect and validate credentials. Raise on failure (the gate retries)."""

    async def close(self) -> None:
        pass

    async def maintain(self) -> None:
        """Periodic housekeeping, called from the gate's reaper."""

    # ------------------------------------------------------------------ sandboxes

    @abc.abstractmethod
    async def create(self, spec: CreateSpec) -> str:
        """Create a running sandbox and return its platform id. Raise ImageBuildError for image problems."""

    async def attach(self, sandbox_id: str, meta: dict | None = None) -> bool:
        """Re-acquire a sandbox created by an earlier daemon process; False if it is gone."""
        return False

    def sandbox_meta(self, sandbox_id: str) -> dict:
        """Data to persist with the sandbox record (handed back to ``attach``)."""
        return {}

    async def forget(self, sandbox_id: str) -> None:
        """The gate no longer tracks this sandbox (ended or terminated)."""

    @abc.abstractmethod
    async def exec(self, sandbox_id: str, argv: list[str], *, timeout_s: int, workdir: str | None,
                   env: dict[str, str] | None, stdin: bytes | None,
                   on_output: OutputCallback) -> ExecOutcome:
        """Run ``argv`` (no shell) as the image's default user; stream output through ``on_output``.
        Raise KeyError for an unknown sandbox."""

    @abc.abstractmethod
    async def write_file(self, sandbox_id: str, path: str, data: bytes, mode: int | None) -> None:
        """Write ``data`` to absolute ``path`` (creating parent directories), then chmod ``mode``."""

    @abc.abstractmethod
    async def read_file(self, sandbox_id: str, path: str, max_bytes: int) -> bytes:
        """Return the file's bytes; FileTooLarge above ``max_bytes``; FileNotFoundError if missing."""

    @abc.abstractmethod
    async def terminate(self, sandbox_id: str) -> None:
        """Stop the sandbox and release its resources. Idempotent."""

    @abc.abstractmethod
    async def poll(self, sandbox_id: str) -> int | None:
        """None while running, else the exit code."""
