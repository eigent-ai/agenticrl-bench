from __future__ import annotations
import datetime as _dt
import json
import os
import threading
from typing import Any
def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="milliseconds")
class AuditLog:
    def __init__(self, path: str, mode: int = 0o644, fsync_every: int = 50):
        self.path = path
        os.makedirs(os.path.dirname(path), mode=0o755, exist_ok=True)
        fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, mode)
        os.fchmod(fd, mode)
        self._f = os.fdopen(fd, "a", buffering=1, encoding="utf-8")
        self._lock = threading.Lock()
        self._seq = self._last_seq()
        self._fsync_every = fsync_every
        self._since_sync = 0
    def _last_seq(self) -> int:
        try:
            with open(self.path, "rb") as f:
                f.seek(0, os.SEEK_END)
                size = f.tell()
                f.seek(max(0, size - 65536))
                lines = f.read().splitlines()
            for line in reversed(lines):
                try:
                    return int(json.loads(line)["seq"])
                except Exception:
                    continue
        except OSError:
            pass
        return 0
    def write(self, event: str, *, sync: bool = False, **fields: Any) -> None:
        with self._lock:
            self._seq += 1
            rec = {"seq": self._seq, "ts": _now_iso(), "event": event, **fields}
            self._f.write(json.dumps(rec, default=str, ensure_ascii=False) + "\n")
            self._since_sync += 1
            if sync or self._since_sync >= self._fsync_every:
                self._f.flush()
                os.fsync(self._f.fileno())
                self._since_sync = 0
    def close(self) -> None:
        with self._lock:
            try:
                self._f.flush()
                os.fsync(self._f.fileno())
            finally:
                self._f.close()
def summarize(path: str) -> dict[str, Any]:
    ops: dict[str, dict[str, int]] = {}
    denied: dict[str, int] = {}
    images: dict[str, int] = {}
    uids: dict[str, int] = {}
    created = ended = 0
    network_values: set[str] = set()
    last_usage: dict[str, Any] | None = None
    starts = 0
    shutdown = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            ev = rec.get("event")
            if ev == "request":
                op = rec.get("op", "?")
                d = ops.setdefault(op, {"allowed": 0, "denied": 0, "failed": 0})
                d[rec.get("outcome", "allowed")] = d.get(rec.get("outcome", "allowed"), 0) + 1
                uid = str((rec.get("peer") or {}).get("uid"))
                uids[uid] = uids.get(uid, 0) + 1
                if rec.get("outcome") == "denied":
                    reason = str(rec.get("error", ""))[:120]
                    denied[reason] = denied.get(reason, 0) + 1
                if op == "create" and rec.get("outcome") == "allowed":
                    created += 1
                    images[rec.get("image", "?")] = images.get(rec.get("image", "?"), 0) + 1
                    network_values.add(str(rec.get("network")))
            elif ev == "sandbox_ended":
                ended += 1
            elif ev == "usage":
                last_usage = rec
            elif ev == "start":
                starts += 1
            elif ev == "shutdown":
                shutdown = rec
    return {
        "daemon_starts": starts,
        "ops": ops,
        "denied_reasons": denied,
        "sandboxes_created": created,
        "sandboxes_ended": ended,
        "child_network_settings": sorted(network_values),
        "images": images,
        "requests_by_uid": uids,
        "last_usage": last_usage,
        "shutdown": shutdown,
    }
