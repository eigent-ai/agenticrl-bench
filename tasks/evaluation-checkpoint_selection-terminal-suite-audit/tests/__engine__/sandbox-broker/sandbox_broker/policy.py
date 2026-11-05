from __future__ import annotations
import dataclasses
import fnmatch
import hashlib
import json
import os
import re
import stat
from pathlib import Path
from typing import Any
DEFAULT_POLICY_PATH = "/etc/sandbox-broker/policy.toml"
DEFAULT_SOCKET_PATH = "/run/sandbox-broker.sock"
_MiB = 1024 * 1024
class PolicyError(ValueError):
    pass
@dataclasses.dataclass
class Limits:
    max_concurrent: int = 32
    max_total_creates: int = 0
    default_cpu: float = 1.0
    min_cpu: float = 0.125
    max_cpu: float = 2.0
    default_memory_mb: int = 2048
    min_memory_mb: int = 128
    max_memory_mb: int = 8192
    default_timeout_s: int = 3600
    max_timeout_s: int = 3600
    idle_timeout_s: int = 900
    max_idle_timeout_s: int = 3600
    default_exec_timeout_s: int = 600
    max_exec_timeout_s: int = 1800
    budget_sandbox_seconds: float = 0.0
    min_create_budget_s: int = 60
    max_file_bytes: int = 64 * _MiB
    max_output_bytes: int = 8 * _MiB
    max_context_bytes: int = 64 * _MiB
    max_context_file_bytes: int = 4 * _MiB - 1
    max_inflight_execs: int = 512
    create_timeout_s: int = 1200
    reap_interval_s: float = 5.0
    poll_interval_s: float = 30.0
    usage_log_interval_s: float = 300.0
@dataclasses.dataclass
class ImageRules:
    allow: list[str] = dataclasses.field(default_factory=list)
    pins: dict[str, str] = dataclasses.field(default_factory=dict)
    pins_file: str | None = None
    require_pin: bool = False
    build_contexts: list[str] = dataclasses.field(default_factory=list)
    build_contexts_file: str | None = None
    setup_commands: list[str] = dataclasses.field(default_factory=list)
    allow_any_build_context: bool = False
NETWORK_CHOICES = ("none", "egress")
@dataclasses.dataclass
class SandboxDefaults:
    network: str = "none"
    hostname: str = "sandbox"
    normalize_prompt: bool = True
@dataclasses.dataclass
class Policy:
    socket_path: str = DEFAULT_SOCKET_PATH
    socket_mode: int = 0o666
    socket_group: str | None = None
    allowed_uids: list[int] = dataclasses.field(default_factory=list)
    admin_uids: list[int] = dataclasses.field(default_factory=lambda: [0])
    state_dir: str = "/var/lib/sandbox-broker"
    log_dir: str = "/var/log/sandbox-broker"
    audit_log_mode: int = 0o644
    log_resolved_hosts: bool = False
    limits: Limits = dataclasses.field(default_factory=Limits)
    images: ImageRules = dataclasses.field(default_factory=ImageRules)
    sandbox: SandboxDefaults = dataclasses.field(default_factory=SandboxDefaults)
    source_path: str | None = None
    source_sha256: str | None = None
    legacy_backend: dict[str, Any] = dataclasses.field(default_factory=dict, repr=False)
    @property
    def audit_log(self) -> str:
        return os.path.join(self.log_dir, "audit.jsonl")
    @property
    def daemon_log(self) -> str:
        return os.path.join(self.log_dir, "daemon.log")
    @property
    def credentials_path(self) -> str:
        return os.path.join(self.state_dir, "credentials.json")
    @property
    def state_path(self) -> str:
        return os.path.join(self.state_dir, "state.json")
    @property
    def contexts_dir(self) -> str:
        return os.path.join(self.state_dir, "contexts")
    def summary(self) -> dict[str, Any]:
        return {
            "network": "blocked" if self.sandbox.network == "none" else "egress",
            "hostname": self.sandbox.hostname or None,
            "limits": dataclasses.asdict(self.limits),
            "images": {
                "allow": list(self.images.allow),
                "pinned_refs": len(self.images.pins),
                "require_pin": self.images.require_pin,
                "build_contexts": "any" if self.images.allow_any_build_context else len(self.images.build_contexts),
                "setup_commands": len(self.images.setup_commands),
            },
            "policy_sha256": self.source_sha256,
        }
def _parse_mode(value: Any) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return int(value, 8)
    raise PolicyError(f"invalid file mode: {value!r}")
def _fill(cls, data: dict[str, Any], where: str):
    fields = {f.name for f in dataclasses.fields(cls)}
    unknown = set(data) - fields
    if unknown:
        raise PolicyError(f"unknown key(s) in {where}: {', '.join(sorted(unknown))}")
    return cls(**data)
def _read_text_list(path: str) -> list[str]:
    out = []
    for line in Path(path).read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            out.append(line.split()[0])
    return out
def check_root_owned(path: str) -> None:
    st = os.stat(path)
    if st.st_uid != 0 or st.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
        raise PolicyError(f"{path} must be owned by root and not writable by group/others")
LEGACY_BACKEND_KEYS = ("app_name", "network")
def parse_policy(data: dict[str, Any]) -> Policy:
    data = dict(data)
    legacy = {k: data.pop(k) for k in list(data) if k in LEGACY_BACKEND_KEYS or k.endswith("_environment")}
    limits = _fill(Limits, dict(data.pop("limits", {}) or {}), "[limits]")
    images = _fill(ImageRules, dict(data.pop("images", {}) or {}), "[images]")
    sandbox = _fill(SandboxDefaults, dict(data.pop("sandbox", {}) or {}), "[sandbox]")
    if sandbox.network not in NETWORK_CHOICES:
        raise PolicyError(f"[sandbox] network must be one of {', '.join(NETWORK_CHOICES)}")
    if sandbox.hostname and not re.fullmatch(r"[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?", sandbox.hostname):
        raise PolicyError(f"[sandbox] hostname is not a valid host name: {sandbox.hostname!r}")
    for key in ("socket_mode", "audit_log_mode"):
        if key in data:
            data[key] = _parse_mode(data[key])
    policy = _fill(Policy, data, "policy")
    policy.limits = limits
    policy.images = images
    policy.sandbox = sandbox
    policy.legacy_backend = legacy
    return policy
def load_policy(path: str | None = None, *, strict: bool = False) -> Policy:
    path = path or os.environ.get("SANDBOX_GATE_POLICY") or os.environ.get("SANDBOX_BROKER_POLICY") or DEFAULT_POLICY_PATH
    if not os.path.exists(path):
        raise PolicyError(f"policy file not found: {path}")
    if strict:
        check_root_owned(path)
    raw = Path(path).read_bytes()
    if path.endswith(".json"):
        data = json.loads(raw)
    else:
        try:
            import tomllib
        except ModuleNotFoundError:
            try:
                import tomli as tomllib
            except ModuleNotFoundError as exc:
                raise PolicyError("TOML policy needs Python 3.11+ or tomli; use a .json policy") from exc
        data = tomllib.loads(raw.decode())
    policy = parse_policy(data)
    policy.source_path = path
    policy.source_sha256 = hashlib.sha256(raw).hexdigest()
    base = os.path.dirname(os.path.abspath(path))
    rules = policy.images
    if rules.pins_file:
        pins_path = os.path.join(base, rules.pins_file)
        if strict:
            check_root_owned(pins_path)
        rules.pins.update(json.loads(Path(pins_path).read_text()))
    if rules.build_contexts_file:
        ctx_path = os.path.join(base, rules.build_contexts_file)
        if strict:
            check_root_owned(ctx_path)
        rules.build_contexts.extend(_read_text_list(ctx_path))
    rules.pins = {normalize_ref(k).name_tag: _check_digest(v) for k, v in rules.pins.items()}
    rules.build_contexts = sorted({c.lower() for c in rules.build_contexts})
    for c in rules.build_contexts:
        if not re.fullmatch(r"[0-9a-f]{64}", c):
            raise PolicyError(f"build context hash must be 64 hex chars: {c!r}")
    return policy
_REF_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._\-/:@]{0,511}$")
_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
def _check_digest(d: str) -> str:
    if not _DIGEST_RE.match(d):
        raise PolicyError(f"invalid image digest: {d!r}")
    return d
@dataclasses.dataclass(frozen=True)
class ImageRef:
    registry: str
    repository: str
    tag: str | None
    digest: str | None
    @property
    def name(self) -> str:
        return f"{self.registry}/{self.repository}"
    @property
    def name_tag(self) -> str:
        return f"{self.name}:{self.tag}" if self.tag else self.name
    @property
    def match_key(self) -> str:
        return self.name_tag if self.tag else f"{self.name}@{self.digest}"
    def pull_ref(self, digest: str | None = None) -> str:
        name = self.name
        if self.registry == "docker.io":
            name = self.repository[len("library/"):] if self.repository.startswith("library/") else self.repository
        digest = digest or self.digest
        if digest:
            return f"{name}@{digest}"
        return f"{name}:{self.tag}"
def normalize_ref(ref: str) -> ImageRef:
    ref = ref.strip()
    if not _REF_RE.match(ref) or ".." in ref or "//" in ref:
        raise ValueError(f"malformed image reference: {ref!r}")
    digest = None
    if "@" in ref:
        ref, digest = ref.split("@", 1)
        _check_digest(digest)
    tag = None
    slash = ref.rfind("/")
    colon = ref.rfind(":")
    if colon > slash:
        ref, tag = ref[:colon], ref[colon + 1:]
        if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.\-]{0,127}", tag):
            raise ValueError(f"malformed image tag: {tag!r}")
    parts = ref.split("/")
    if len(parts) > 1 and ("." in parts[0] or ":" in parts[0] or parts[0] == "localhost"):
        registry, repo = parts[0], "/".join(parts[1:])
    else:
        registry, repo = "docker.io", ref
    if registry in ("index.docker.io", "registry-1.docker.io"):
        registry = "docker.io"
    if registry == "docker.io" and "/" not in repo:
        repo = f"library/{repo}"
    if repo != repo.lower():
        raise ValueError(f"repository names must be lowercase: {repo!r}")
    if tag is None and digest is None:
        tag = "latest"
    return ImageRef(registry, repo, tag, digest)
def normalize_pattern(pattern: str) -> str:
    pattern = pattern.strip()
    first = pattern.split("/", 1)[0]
    if "/" in pattern and ("." in first or ":" in first or first == "localhost"):
        return pattern
    if "/" not in pattern.split(":", 1)[0].split("@", 1)[0]:
        pattern = f"library/{pattern}"
    return f"docker.io/{pattern}"
@dataclasses.dataclass(frozen=True)
class ResolvedImage:
    kind: str
    display: str
    pull_ref: str | None = None
    context_sha256: str | None = None
def resolve_registry_image(rules: ImageRules, ref: str) -> ResolvedImage:
    try:
        parsed = normalize_ref(ref)
    except ValueError as exc:
        raise PermissionError(str(exc)) from exc
    patterns = [normalize_pattern(p) for p in rules.allow]
    if not any(fnmatch.fnmatchcase(parsed.match_key, p) for p in patterns):
        raise PermissionError(f"image {ref!r} is not in the allowed image list")
    pin = rules.pins.get(parsed.name_tag) if parsed.tag else None
    if pin and parsed.digest and parsed.digest != pin:
        raise PermissionError(f"image {ref!r} does not match its pinned digest")
    digest = parsed.digest or pin
    if rules.require_pin and not digest:
        raise PermissionError(f"image {ref!r} has no pinned digest")
    return ResolvedImage("registry", parsed.match_key, pull_ref=parsed.pull_ref(digest))
def hash_context_dir(root: str | os.PathLike) -> str:
    root = os.fspath(root)
    h = hashlib.sha256(b"sandbox-broker-context-v1\n")
    entries = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in filenames + [d for d in dirnames if os.path.islink(os.path.join(dirpath, d))]:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            entries.append((rel, full))
    for rel, full in sorted(entries):
        st = os.lstat(full)
        if stat.S_ISLNK(st.st_mode):
            h.update(f"L {rel} {os.readlink(full)}\n".encode())
        elif stat.S_ISREG(st.st_mode):
            fh = hashlib.sha256()
            with open(full, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    fh.update(chunk)
            x = "x" if st.st_mode & 0o111 else "-"
            h.update(f"F {rel} {x} {fh.hexdigest()}\n".encode())
    return h.hexdigest()
