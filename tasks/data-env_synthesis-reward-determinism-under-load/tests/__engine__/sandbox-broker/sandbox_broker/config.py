from __future__ import annotations
import dataclasses
import json
import os
import stat
from pathlib import Path
from typing import Any, Mapping
DEFAULT_BACKEND_CONFIG = "/etc/sandbox-broker/backend.toml"
LEGACY_PROVIDER = "modal"
TOKEN_ENV = (("SANDBOX_GATE_TOKEN_ID", "SANDBOX_GATE_TOKEN_SECRET"),
             ("SANDBOX_BROKER_TOKEN_ID", "SANDBOX_BROKER_TOKEN_SECRET"),
             ("MODAL_TOKEN_ID", "MODAL_TOKEN_SECRET"))
CRED_PREFIX = "SANDBOX_GATE_CRED_"
PROVIDER_ENV_VARS = ("SANDBOX_GATE_PROVIDER_ENV", "SANDBOX_BROKER_MODAL_ENVIRONMENT", "MODAL_ENVIRONMENT")
PROVIDER_VAR = "SANDBOX_GATE_PROVIDER"
EXTRA_DOMAIN_VARS = ("SANDBOX_GATE_EXTRA_PARENT_DOMAINS", "SANDBOX_BROKER_EXTRA_PARENT_DOMAINS")
CONFIG_VAR = "SANDBOX_GATE_BACKEND_CONFIG"
SCRUB_VARS = tuple(v for pair in TOKEN_ENV for v in pair) + PROVIDER_ENV_VARS + (PROVIDER_VAR,)
_LEGACY_NETWORK = {"manage_parent_allowlist": "manage_allowlist", "parent_domains": "domains",
                   "parent_cidrs": "cidrs", "refresh_interval_s": "refresh_interval_s"}
class ConfigError(ValueError):
    pass
@dataclasses.dataclass
class BackendConfig:
    providers: dict[str, dict[str, Any]] = dataclasses.field(default_factory=dict)
    credentials_source: str = "env"
    credentials_file: str | None = None
    extra_domains: list[str] = dataclasses.field(default_factory=list)
    source_path: str | None = None
    provider: str | None = None
    def settings(self) -> dict[str, Any]:
        if not self.provider:
            raise ConfigError("no provider chosen")
        table = dict(self.providers.get(self.provider) or {})
        network = dict(table.pop("parent_network", None) or {})
        if self.extra_domains:
            network["extra_domains"] = list(dict.fromkeys([*network.get("extra_domains", []), *self.extra_domains]))
        return {"settings": table, "parent_network": network}
def _load_toml_or_json(path: str) -> dict[str, Any]:
    raw = Path(path).read_bytes()
    if path.endswith(".json"):
        return json.loads(raw)
    try:
        import tomllib
    except ModuleNotFoundError:
        try:
            import tomli as tomllib
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
    return BackendConfig(providers=providers, credentials_source=source, credentials_file=creds.get("file"))
def load_backend_config(path: str | None = None, *, policy_path: str | None = None, strict: bool = False,
                        legacy: Mapping[str, Any] | None = None,
                        env: Mapping[str, str] | None = None) -> BackendConfig:
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
def credentials_from_env(env: Mapping[str, str]) -> dict[str, str] | None:
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
