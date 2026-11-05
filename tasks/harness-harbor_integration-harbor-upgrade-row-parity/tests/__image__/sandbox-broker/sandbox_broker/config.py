"""Root-only backend config and credentials (daemon side; never imported by clients).

The gate reads two files:

* the public policy (``policy.py``; root:root 0644, readable by workloads): socket, limits,
  images, sandbox defaults. Nothing platform-specific.
* the backend config (this module; root:root 0600): per-platform account-side names, the
  hosts this container needs for each platform's control plane, and where the credentials
  come from. Default path: ``backend.toml`` next to the policy file, else
  ``/etc/sandbox-broker/backend.toml``.

The backend config never chooses the platform. The task does, in ``task.toml``
(``SANDBOX_GATE_PROVIDER`` in ``[environment.env]`` / ``[verifier.env]``), so switching
platforms never needs an image change. The config only holds one table per platform it
knows how to use:

    [modal]                                    # handed to the modal backend's from_config
    app_name = "terminal-sandboxes"
    [modal.parent_network]                     # optional; backends that manage this container's allowlist
    manage_allowlist = false
    domains = ["api.modal.com"]

    [daytona]
    # api_url = "https://app.daytona.io/api"

    [sandbox]                                  # optional; what every sandbox must provide, whatever the platform
    hostname = "modal"                         # checked after every create (set where the platform allows it)
    pid1_signals = "native-or-refuse"          # see server.py, "Platform conformance"

    [credentials]
    source = "env"                             # "env": captured by `start` from the variables below
    # source = "file"; file = "/etc/sandbox-broker/credentials.json"   # root:root 0600 JSON

Environment variables (read only by the root ``start`` step, then dropped):

    SANDBOX_GATE_PROVIDER                              the platform (a key of backends.REGISTRY); required
    SANDBOX_GATE_TOKEN_ID / SANDBOX_GATE_TOKEN_SECRET   token-pair credentials (Modal)
    SANDBOX_GATE_CRED_<NAME>                           any other credential field, stored as <name> (lower
                                                       case), e.g. SANDBOX_GATE_CRED_API_KEY -> api_key (Daytona)
    SANDBOX_GATE_PROVIDER_ENV                          provider-side environment / project / region
    SANDBOX_GATE_EXTRA_PARENT_DOMAINS                  comma-separated, appended to [<provider>.parent_network].domains
    SANDBOX_GATE_BACKEND_CONFIG                        backend config path

``start`` stores the provider in the root-only credentials record next to the credentials;
the daemon and any other reader of that record (``source = "file"``) take it from there.
Empty values count as unset, so a task can default its host variables to "" and fail only
its own start step, never ``harbor run`` for a whole directory.

Legacy names still accepted: SANDBOX_BROKER_TOKEN_ID/SECRET, SANDBOX_BROKER_MODAL_ENVIRONMENT,
SANDBOX_BROKER_EXTRA_PARENT_DOMAINS, MODAL_TOKEN_ID/SECRET, MODAL_ENVIRONMENT; and, when no
backend config file exists, the legacy policy keys ``app_name``, ``modal_environment`` and
``[network]`` (manage_parent_allowlist, parent_domains, parent_cidrs, refresh_interval_s), read
as the ``[modal]`` table.
"""
from __future__ import annotations

import dataclasses
import json
import os
import stat
from pathlib import Path
from typing import Any, Mapping

DEFAULT_BACKEND_CONFIG = "/etc/sandbox-broker/backend.toml"
LEGACY_PROVIDER = "modal"  # the provider the legacy policy keys describe

TOKEN_ENV = (("SANDBOX_GATE_TOKEN_ID", "SANDBOX_GATE_TOKEN_SECRET"),
             ("SANDBOX_BROKER_TOKEN_ID", "SANDBOX_BROKER_TOKEN_SECRET"),  # legacy
             ("MODAL_TOKEN_ID", "MODAL_TOKEN_SECRET"))  # legacy
CRED_PREFIX = "SANDBOX_GATE_CRED_"
PROVIDER_ENV_VARS = ("SANDBOX_GATE_PROVIDER_ENV", "SANDBOX_BROKER_MODAL_ENVIRONMENT", "MODAL_ENVIRONMENT")
PROVIDER_VAR = "SANDBOX_GATE_PROVIDER"
EXTRA_DOMAIN_VARS = ("SANDBOX_GATE_EXTRA_PARENT_DOMAINS", "SANDBOX_BROKER_EXTRA_PARENT_DOMAINS")
CONFIG_VAR = "SANDBOX_GATE_BACKEND_CONFIG"
#: every variable that may carry a secret or a platform name; dropped from the environment after capture
#: (plus every SANDBOX_GATE_CRED_* variable)
SCRUB_VARS = tuple(v for pair in TOKEN_ENV for v in pair) + PROVIDER_ENV_VARS + (PROVIDER_VAR,)

_LEGACY_NETWORK = {"manage_parent_allowlist": "manage_allowlist", "parent_domains": "domains",
                   "parent_cidrs": "cidrs", "refresh_interval_s": "refresh_interval_s"}


class ConfigError(ValueError):
    pass


@dataclasses.dataclass
class BackendConfig:
    #: per-provider tables (``[modal]``, ``[daytona]``, ...); each may hold a ``parent_network`` sub-table
    providers: dict[str, dict[str, Any]] = dataclasses.field(default_factory=dict)
    credentials_source: str = "env"  # "env" | "file" | "none"
    credentials_file: str | None = None
    extra_domains: list[str] = dataclasses.field(default_factory=list)
    source_path: str | None = None
    #: chosen at start from the task (SANDBOX_GATE_PROVIDER), never by this file
    provider: str | None = None
    #: platform conformance every sandbox must meet ([sandbox]; server.py, "Platform conformance")
    sandbox: dict[str, Any] = dataclasses.field(default_factory=dict)

    def settings(self) -> dict[str, Any]:
        """What the chosen backend's from_config receives."""
        if not self.provider:
            raise ConfigError("no provider chosen")
        table = dict(self.providers.get(self.provider) or {})
        network = dict(table.pop("parent_network", None) or {})
        if self.extra_domains:
            # appended to the backend's own default when the table names no domains (the backend merges)
            network["extra_domains"] = list(dict.fromkeys([*network.get("extra_domains", []), *self.extra_domains]))
        return {"settings": table, "parent_network": network}


def _load_toml_or_json(path: str) -> dict[str, Any]:
    raw = Path(path).read_bytes()
    if path.endswith(".json"):
        return json.loads(raw)
    try:
        import tomllib  # type: ignore[import-not-found]
    except ModuleNotFoundError:  # pragma: no cover - py<3.11
        try:
            import tomli as tomllib  # type: ignore[no-redef]
        except ModuleNotFoundError as exc:
            raise ConfigError("TOML needs Python 3.11+ or tomli; use a .json backend config") from exc
    return tomllib.loads(raw.decode())


def check_root_only(path: str) -> None:
    st = os.stat(path)
    if st.st_uid != 0 or st.st_mode & 0o077 or not stat.S_ISREG(st.st_mode):
        raise ConfigError(f"{path} must be a regular file owned by root with mode 0600")


def default_backend_config_path(policy_path: str | None) -> str:
    if os.environ.get(CONFIG_VAR):
        return os.environ[CONFIG_VAR]
    if policy_path:
        sibling = os.path.join(os.path.dirname(os.path.abspath(policy_path)), "backend.toml")
        if os.path.exists(sibling):
            return sibling
    return DEFAULT_BACKEND_CONFIG


def _extra_domains(env: Mapping[str, str]) -> list[str]:
    out: list[str] = []
    for var in EXTRA_DOMAIN_VARS:
        out += [h.strip() for h in env.get(var, "").split(",") if h.strip()]
    return out


def parse_backend_config(data: Mapping[str, Any]) -> BackendConfig:
    from .backends import REGISTRY

    data = dict(data)
    if "provider" in data:
        raise ConfigError("the backend config cannot choose the provider; the task does "
                          "(task.toml: SANDBOX_GATE_PROVIDER in [environment.env] / [verifier.env])")
    if "settings" in data or "parent_network" in data:
        raise ConfigError("top-level [settings] / [parent_network] are gone; put them in the provider's table "
                          "([<provider>] and [<provider>.parent_network])")
    creds = dict(data.pop("credentials", None) or {})
    sandbox = parse_sandbox_requirements(data.pop("sandbox", None) or {})
    unknown = set(data) - set(REGISTRY)
    if unknown:
        raise ConfigError(f"unknown key(s) in backend config: {', '.join(sorted(unknown))} "
                          f"(provider tables: {', '.join(sorted(REGISTRY))})")
    providers = {}
    for name, table in data.items():
        if not isinstance(table, Mapping):
            raise ConfigError(f"[{name}] must be a table")
        providers[name] = dict(table)
    if set(creds) - {"source", "file"}:
        raise ConfigError(f"unknown [credentials] key(s): {', '.join(sorted(set(creds) - {'source', 'file'}))}")
    source = creds.get("source", "file" if creds.get("file") else "env")
    if source not in ("env", "file", "none"):
        raise ConfigError(f"[credentials] source must be env, file or none, not {source!r}")
    if source == "file" and not creds.get("file"):
        raise ConfigError("[credentials] source = \"file\" needs file = \"<path>\"")
    return BackendConfig(providers=providers, credentials_source=source, credentials_file=creds.get("file"),
                         sandbox=sandbox)


SANDBOX_KEYS = {"hostname", "pid1_signals"}
PID1_MODES = ("platform", "native-or-refuse")


def parse_sandbox_requirements(table: Mapping[str, Any]) -> dict[str, Any]:
    """The root-only ``[sandbox]`` table: what every sandbox must provide on any platform."""
    import re

    if not isinstance(table, Mapping):
        raise ConfigError("[sandbox] must be a table")
    unknown = set(table) - SANDBOX_KEYS
    if unknown:
        raise ConfigError(f"unknown [sandbox] key(s): {', '.join(sorted(unknown))}")
    out: dict[str, Any] = {}
    hostname = table.get("hostname") or ""
    if hostname:
        if not isinstance(hostname, str) or not re.fullmatch(r"[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?", hostname):
            raise ConfigError(f"[sandbox] hostname is not a valid host name: {hostname!r}")
        out["hostname"] = hostname
    mode = table.get("pid1_signals", "platform")
    if mode not in PID1_MODES:
        raise ConfigError(f"[sandbox] pid1_signals must be one of {', '.join(PID1_MODES)}, not {mode!r}")
    if mode != "platform":
        out["pid1_signals"] = mode
    return out


def load_backend_config(path: str | None = None, *, policy_path: str | None = None, strict: bool = False,
                        legacy: Mapping[str, Any] | None = None,
                        env: Mapping[str, str] | None = None) -> BackendConfig:
    """Load the root-only backend config; fall back to the legacy keys of the public policy."""
    env = os.environ if env is None else env
    path = path or default_backend_config_path(policy_path)
    if os.path.exists(path):
        if strict:
            check_root_only(path)
        cfg = parse_backend_config(_load_toml_or_json(path))
        cfg.source_path = path
    else:
        cfg = BackendConfig()
        legacy = dict(legacy or {})
        table: dict[str, Any] = {}
        if legacy.get("app_name"):
            table["app_name"] = legacy["app_name"]
        if legacy.get("modal_environment"):
            table["environment"] = legacy["modal_environment"]
        net = dict(legacy.get("network") or {})
        unknown = set(net) - set(_LEGACY_NETWORK)
        if unknown:
            raise ConfigError(f"unknown key(s) in [network]: {', '.join(sorted(unknown))}")
        if net:
            table["parent_network"] = {_LEGACY_NETWORK[k]: v for k, v in net.items()}
        if table:
            cfg.providers[LEGACY_PROVIDER] = table
    cfg.extra_domains = _extra_domains(env)
    return cfg


def provider_from_env(env: Mapping[str, str]) -> str | None:
    return (env.get(PROVIDER_VAR) or "").strip() or None


# ---------------------------------------------------------------------------- credentials


def credentials_from_env(env: Mapping[str, str]) -> dict[str, str] | None:
    """The credential fields in ``env``: a token pair and/or SANDBOX_GATE_CRED_* fields. None if there are none."""
    creds: dict[str, str] = {}
    for id_var, secret_var in TOKEN_ENV:
        if env.get(id_var) and env.get(secret_var):
            creds = {"token_id": env[id_var], "token_secret": env[secret_var]}
            break
    for var, value in env.items():
        if var.startswith(CRED_PREFIX) and value and var != CRED_PREFIX:
            creds[var[len(CRED_PREFIX):].lower()] = value
    if not creds:
        return None
    for var in PROVIDER_ENV_VARS:
        if env.get(var):
            creds["environment"] = env[var]
            break
    return creds


def scrub_env(env: dict[str, str] | None = None) -> None:
    """Drop every credential / platform variable from ``env`` (default: this process)."""
    env = os.environ if env is None else env
    for var in [*SCRUB_VARS, *(v for v in env if v.startswith(CRED_PREFIX))]:
        env.pop(var, None)


def write_credentials(path: str, creds: Mapping[str, Any]) -> None:
    d = os.path.dirname(path)
    os.makedirs(d, mode=0o700, exist_ok=True)
    os.chmod(d, 0o700)
    tmp = f"{path}.tmp"
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(dict(creds), f)
    os.chmod(tmp, 0o600)
    os.replace(tmp, path)


def read_credentials(path: str, *, strict: bool) -> dict[str, Any]:
    if strict:
        check_root_only(path)
    with open(path) as f:
        return json.load(f)
