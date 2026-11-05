"""Wire format between clients and the gate daemon (platform-neutral).

One JSON object per line over a Unix stream socket. A request is a single line with an
``op`` field; the reply is a single line, preceded by ``{"event": ...}`` lines when the
client asked an ``exec`` to stream its output. Binary data travels base64-encoded.

Requests (optional fields in brackets):
  ping
  create     image | build_context_b64, [cpu, memory_mb, timeout_s, idle_timeout_s,
             workdir, env, labels]                                     -> id, ...
  exec       id, argv, [timeout_s, workdir, env, stdin_b64, stream, binary]
                                                                       -> rc, stdout, stderr, timed_out
  put_file   id, path, data_b64, [mode]                               (alias: put)
  get_file   id, path                                                  -> data_b64 (alias: get)
  terminate  id
  poll       id                                                        -> running, rc
  list       [all]                                                     -> sandboxes
  usage                                                                -> budget and counters
  policy                                                               -> effective limits
  shutdown   [exit]                                                    (admin only)

Successful replies carry ``"ok": true``. Errors are ``{"ok": false, "error": <message>,
"error_type": <kind>}``.
"""
from __future__ import annotations

import json
from typing import Any

PROTOCOL_VERSION = 1

COMMON_FIELDS = {"op", "request_id"}

REQUEST_FIELDS: dict[str, set[str]] = {
    "ping": set(),
    "create": {"image", "build_context_b64", "cpu", "memory_mb", "timeout_s", "idle_timeout_s",
               "workdir", "env", "labels"},
    "exec": {"id", "argv", "timeout_s", "workdir", "env", "stdin_b64", "stream", "binary"},
    "put_file": {"id", "path", "data_b64", "mode"},
    "get_file": {"id", "path"},
    "terminate": {"id"},
    "poll": {"id"},
    "list": {"all"},
    "usage": set(),
    "policy": set(),
    "shutdown": {"exit"},
}

ALIASES = {"put": "put_file", "get": "get_file", "status": "usage"}

ADMIN_OPS = {"shutdown"}


class BrokerError(Exception):
    """An error reported to the client. ``kind`` is a stable machine-readable category."""

    kind = "error"
    detail = ""  # platform details; only admins see them (server.process)

    def __init__(self, message: str, kind: str | None = None):
        super().__init__(message)
        if kind:
            self.kind = kind


class BadRequest(BrokerError):
    kind = "bad_request"


class PolicyDenied(BrokerError):
    kind = "denied"


class QuotaExceeded(BrokerError):
    kind = "quota"


class SandboxNotFound(BrokerError):
    kind = "not_found"


class BackendFailure(BrokerError):
    kind = "backend"


class BrokerUnavailable(BrokerError):
    kind = "unavailable"


ERROR_TYPES = {cls.kind: cls for cls in (BadRequest, PolicyDenied, QuotaExceeded, SandboxNotFound,
                                         BackendFailure, BrokerUnavailable)}


def error_from_reply(reply: dict[str, Any]) -> BrokerError:
    cls = ERROR_TYPES.get(reply.get("error_type", ""), BrokerError)
    return cls(str(reply.get("error", "unknown error")), reply.get("error_type"))


def encode(obj: dict[str, Any]) -> bytes:
    return (json.dumps(obj, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def decode(line: bytes) -> dict[str, Any]:
    obj = json.loads(line)
    if not isinstance(obj, dict):
        raise BadRequest("request must be a JSON object")
    return obj


def validate_request(req: dict[str, Any]) -> str:
    op = req.get("op")
    if not isinstance(op, str):
        raise BadRequest("missing 'op'")
    op = ALIASES.get(op, op)
    if op not in REQUEST_FIELDS:
        raise BadRequest(f"unknown op {op!r}")
    unknown = set(req) - COMMON_FIELDS - REQUEST_FIELDS[op]
    if unknown:
        raise BadRequest(f"unsupported field(s) for {op}: {', '.join(sorted(unknown))}")
    return op
