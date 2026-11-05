"""Staging services that task sandboxes talk to (host side, one instance per tenant and service).

Every service speaks plain HTTP/1.x with JSON bodies. A service whose spec has "admin": true also serves
    GET  /_admin/journal          state-changing requests so far: [{"seq", "method", "path", "body", "status", "response"}]
    POST /_admin/rewind {"seq":n} put the service back to its state after the first n journal entries
"""
import copy
import hashlib
import json
import re
import uuid
from urllib.parse import parse_qs, unquote, urlsplit


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


class Service:
    kind = "base"

    def __init__(self, spec: dict, saved: dict | None = None):
        self.spec = spec
        self.admin = bool(spec.get("admin"))
        if saved:
            self.state = saved["state"]
            self.journal = saved["journal"]
            self.history = saved["history"]
        else:
            self.state = self.initial(spec.get("seed") or {})
            self.journal = []
            self.history = [copy.deepcopy(self.state)]

    # ---- overridden by kinds
    def initial(self, seed: dict) -> dict:
        return {}

    def handle(self, method: str, parts: list, query: dict, body):
        return 404, {"error": "not found"}

    # ---- common
    def request(self, method: str, target: str, raw_body: bytes):
        u = urlsplit(target)
        path = unquote(u.path)
        query = {k: v[-1] for k, v in parse_qs(u.query).items()}
        body = None
        if raw_body:
            try:
                body = json.loads(raw_body)
            except ValueError:
                body = raw_body.decode("utf-8", "replace")
        if path.startswith("/_admin"):
            if not self.admin:
                return 404, {"error": "not found"}
            if method == "GET" and path == "/_admin/journal":
                return 200, self.journal
            if method == "POST" and path == "/_admin/rewind":
                try:
                    n = int((body or {}).get("seq"))
                except (TypeError, ValueError, AttributeError):
                    return 400, {"error": "seq required"}
                if not 0 <= n <= len(self.journal):
                    return 400, {"error": f"seq out of range 0..{len(self.journal)}"}
                self.state = copy.deepcopy(self.history[n])
                del self.journal[n:]
                del self.history[n + 1:]
                return 200, {"seq": n}
            return 404, {"error": "not found"}
        before = canon(self.state)
        parts = [p for p in path.split("/") if p]
        try:
            status, resp = self.handle(method, parts, query, body)
        except (KeyError, TypeError, ValueError) as e:
            status, resp = 400, {"error": f"bad request: {e}"}
        if canon(self.state) != before:
            self.journal.append({"seq": len(self.journal) + 1, "method": method, "path": target,
                                 "body": body, "status": status, "response": resp})
            self.history.append(copy.deepcopy(self.state))
        return status, resp

    def dump(self) -> dict:
        return {"kind": self.kind, "spec": self.spec, "state": self.state, "journal": self.journal,
                "history": self.history}

    def digest(self) -> str:
        return hashlib.sha256(canon(self.state).encode()).hexdigest()


class Tickets(Service):
    kind = "tickets"

    def initial(self, seed):
        return {"next": int(seed.get("first_id", 101)), "tickets": copy.deepcopy(seed.get("tickets", {}))}

    def _new_id(self):
        if self.spec.get("ids") == "uuid":
            return uuid.uuid4().hex[:12]
        i = self.state["next"]
        self.state["next"] += 1
        return f"{self.spec.get('prefix', 'T')}-{i}"

    def handle(self, method, parts, query, body):
        t = self.state["tickets"]
        if parts == ["tickets"] and method == "GET":
            st = query.get("status")
            return 200, [{"id": k, "title": v["title"], "status": v["status"]} for k, v in t.items()
                         if not st or v["status"] == st]
        if parts == ["tickets"] and method == "POST":
            tid = self._new_id()
            t[tid] = {"title": str(body["title"]), "status": "open", "comments": [], "labels": []}
            return 201, {"id": tid}
        if len(parts) >= 2 and parts[0] == "tickets":
            tid = parts[1]
            if tid not in t:
                return 404, {"error": "no such ticket"}
            if len(parts) == 2 and method == "GET":
                return 200, dict(t[tid], id=tid)
            if parts[2:] == ["comments"] and method == "POST":
                t[tid]["comments"].append(str(body["body"]))
                return 201, {"id": tid, "comments": len(t[tid]["comments"])}
            if parts[2:] == ["close"] and method == "POST":
                t[tid]["status"] = "closed"
                return 200, {"id": tid, "status": "closed"}
            if parts[2:] == ["labels"] and method == "POST":
                lab = str(body["label"])
                if lab not in t[tid]["labels"]:
                    t[tid]["labels"].append(lab)
                return 200, {"id": tid, "labels": t[tid]["labels"]}
        return 404, {"error": "not found"}


class Counter(Service):
    """Sequence numbers. GET /next/<name> hands out the next number (it is not a read)."""
    kind = "counter"

    def initial(self, seed):
        return {"counters": dict(seed.get("counters", {}))}

    def handle(self, method, parts, query, body):
        c = self.state["counters"]
        if len(parts) == 2 and parts[0] == "next" and method in ("GET", "POST"):
            c[parts[1]] = c.get(parts[1], 0) + 1
            return 200, {"name": parts[1], "value": c[parts[1]]}
        if len(parts) == 2 and parts[0] == "peek" and method == "GET":
            return 200, {"name": parts[1], "value": c.get(parts[1], 0)}
        if parts == ["counters"] and method == "GET":
            return 200, c
        return 404, {"error": "not found"}


class KV(Service):
    kind = "kv"

    def initial(self, seed):
        return {"data": dict(seed.get("data", {}))}

    def handle(self, method, parts, query, body):
        d = self.state["data"]
        if parts == ["kv"] and method == "GET":
            return 200, sorted(d)
        if len(parts) == 2 and parts[0] == "kv":
            k = parts[1]
            if method == "GET":
                return (200, {"key": k, "value": d[k]}) if k in d else (404, {"error": "no such key"})
            if method == "PUT":
                d[k] = body.get("value") if isinstance(body, dict) else body
                return 200, {"key": k}
            if method == "DELETE":
                d.pop(k, None)
                return 200, {"key": k, "deleted": True}
        return 404, {"error": "not found"}


class Inventory(Service):
    kind = "inventory"

    def initial(self, seed):
        return {"items": dict(seed.get("items", {})), "next": 1, "reservations": {}}

    def handle(self, method, parts, query, body):
        it = self.state["items"]
        if parts == ["items"] and method == "GET":
            return 200, it
        if len(parts) == 2 and parts[0] == "items" and method == "GET":
            return (200, {"sku": parts[1], "qty": it[parts[1]]}) if parts[1] in it else (404, {"error": "no such sku"})
        if len(parts) == 3 and parts[0] == "items" and parts[2] == "adjust" and method == "POST":
            sku = parts[1]
            it[sku] = it.get(sku, 0) + int(body["delta"])
            return 200, {"sku": sku, "qty": it[sku]}
        if parts == ["reservations"] and method == "POST":
            sku, qty = str(body["sku"]), int(body["qty"])
            if it.get(sku, 0) < qty:
                return 409, {"error": "insufficient stock"}
            it[sku] -= qty
            if self.spec.get("ids") == "uuid":
                rid = "R-" + uuid.uuid4().hex[:10]
            else:
                rid = f"R-{self.state['next']:04d}"
                self.state["next"] += 1
            self.state["reservations"][rid] = {"sku": sku, "qty": qty}
            return 201, {"reservation": rid, "sku": sku, "qty": qty}
        if parts == ["reservations"] and method == "GET":
            return 200, self.state["reservations"]
        return 404, {"error": "not found"}


class Events(Service):
    """Write-only event sink (analytics / audit / build notifications)."""
    kind = "events"

    def initial(self, seed):
        return {"events": []}

    def handle(self, method, parts, query, body):
        if len(parts) >= 1 and parts[0] == "events" and method == "POST":
            self.state["events"].append({"topic": "/".join(parts[1:]) or "default", "body": body})
            return 202, {"accepted": len(self.state["events"])}
        if parts == ["events"] and method == "GET":
            return 200, {"count": len(self.state["events"])}
        return 404, {"error": "not found"}


class Static(Service):
    """Read-only documents (package index, docs, schema registry)."""
    kind = "static"

    def initial(self, seed):
        return {"docs": dict(seed.get("docs", {}))}

    def handle(self, method, parts, query, body):
        if method != "GET":
            return 405, {"error": "read-only"}
        key = "/".join(parts)
        if key in self.state["docs"]:
            return 200, self.state["docs"][key]
        if key == "":
            return 200, sorted(self.state["docs"])
        return 404, {"error": "not found"}


class Queue(Service):
    """Work queue. GET /jobs/next hands the next pending job to the caller."""
    kind = "queue"

    def initial(self, seed):
        return {"pending": list(seed.get("jobs", [])), "leased": [], "done": []}

    def handle(self, method, parts, query, body):
        st = self.state
        if parts == ["jobs"] and method == "GET":
            return 200, {"pending": len(st["pending"]), "leased": len(st["leased"]), "done": len(st["done"])}
        if parts == ["jobs", "next"] and method in ("GET", "POST"):
            if not st["pending"]:
                return 200, {"job": None}
            job = st["pending"].pop(0)
            st["leased"].append(job)
            return 200, {"job": job}
        if parts == ["jobs"] and method == "POST":
            st["pending"].append(body)
            return 201, {"pending": len(st["pending"])}
        if len(parts) == 3 and parts[0] == "jobs" and parts[2] == "done" and method == "POST":
            for j in list(st["leased"]):
                if str(j.get("id")) == parts[1]:
                    st["leased"].remove(j)
                    st["done"].append(j)
                    return 200, {"id": parts[1], "state": "done"}
            return 404, {"error": "not leased"}
        return 404, {"error": "not found"}


class Orders(Service):
    """Order intake. Order ids are assigned by the service."""
    kind = "orders"

    def initial(self, seed):
        return {"orders": dict(seed.get("orders", {}))}

    def handle(self, method, parts, query, body):
        o = self.state["orders"]
        if parts == ["orders"] and method == "GET":
            return 200, [{"order": k, **v} for k, v in o.items()]
        if parts == ["orders"] and method == "POST":
            oid = uuid.uuid4().hex[:12]
            o[oid] = {"sku": str(body["sku"]), "qty": int(body["qty"]), "state": "placed"}
            return 201, {"order": oid, "state": "placed"}
        if len(parts) == 3 and parts[0] == "orders" and parts[2] == "cancel" and method == "POST":
            if parts[1] not in o:
                return 404, {"error": "no such order"}
            o[parts[1]]["state"] = "cancelled"
            return 200, {"order": parts[1], "state": "cancelled"}
        return 404, {"error": "not found"}


KINDS = {c.kind: c for c in (Tickets, Counter, KV, Inventory, Events, Static, Queue, Orders)}


def make(spec: dict, saved: dict | None = None) -> Service:
    return KINDS[spec["kind"]](spec, saved)


async def serve_http(svc: Service, reader, writer):
    try:
        head = await reader.readuntil(b"\r\n\r\n")
        lines = head.decode("latin-1").split("\r\n")
        method, target = lines[0].split(" ")[:2]
        hdr = {}
        for ln in lines[1:]:
            if ":" in ln:
                k, v = ln.split(":", 1)
                hdr[k.strip().lower()] = v.strip()
        n = int(hdr.get("content-length", "0") or 0)
        raw = await reader.readexactly(n) if n else b""
        status, resp = svc.request(method.upper(), target, raw)
        body = (json.dumps(resp, indent=None) + "\n").encode()
        reason = {200: "OK", 201: "Created", 202: "Accepted", 400: "Bad Request", 404: "Not Found",
                  405: "Method Not Allowed", 409: "Conflict"}.get(status, "OK")
        writer.write(f"HTTP/1.1 {status} {reason}\r\nContent-Type: application/json\r\nContent-Length: {len(body)}\r\n"
                     f"Connection: close\r\n\r\n".encode() + body)
        await writer.drain()
    except Exception:  # noqa: BLE001
        pass
    finally:
        writer.close()


_ID = re.compile(r"^[A-Za-z0-9_.-]+$")
