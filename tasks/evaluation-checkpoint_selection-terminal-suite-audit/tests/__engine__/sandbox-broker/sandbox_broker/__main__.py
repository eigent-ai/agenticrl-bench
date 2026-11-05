from __future__ import annotations
import argparse
import json
import sys
def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="sandbox-broker", description="Operator commands of the sandbox gate.")
    sub = p.add_subparsers(dest="cmd", required=True)
    def daemon_opts(s):
        s.add_argument("--config", help="public policy file (default /etc/sandbox-broker/policy.toml)")
        s.add_argument("--backend-config", help="root-only backend config (default: backend.toml next to the policy, "
                                                 "else /etc/sandbox-broker/backend.toml)")
        s.add_argument("--backend", help=argparse.SUPPRESS)
    s = sub.add_parser("start")
    daemon_opts(s)
    s.add_argument("--wait", type=float, default=120.0)
    s.add_argument("--quiet", action="store_true")
    s = sub.add_parser("serve")
    daemon_opts(s)
    s.add_argument("--dev", action="store_true", help="allow non-root and skip ownership checks (development only)")
    s = sub.add_parser("supervise")
    daemon_opts(s)
    for name in ("status", "list", "shutdown"):
        s = sub.add_parser(name)
        s.add_argument("--socket")
        if name == "list":
            s.add_argument("--all", action="store_true")
        if name == "shutdown":
            s.add_argument("--keep-running", action="store_true",
                           help="terminate sandboxes and refuse new ones, but keep answering queries")
    s = sub.add_parser("audit-summary")
    s.add_argument("path", nargs="?", default="/var/log/sandbox-broker/audit.jsonl")
    s = sub.add_parser("hash-context")
    s.add_argument("dirs", nargs="+")
    a = p.parse_args(argv)
    if a.cmd == "start":
        from .daemon import StartError, start
        try:
            status = start(a.config, wait_s=a.wait, backend_name=a.backend, backend_config=a.backend_config)
        except StartError as exc:
            print(f"sandbox-broker: {exc}", file=sys.stderr)
            return 1
        if not a.quiet:
            print(json.dumps(status))
        return 0
    if a.cmd == "serve":
        from .daemon import StartError, serve
        try:
            return serve(a.config, dev=a.dev, backend_name=a.backend, backend_config=a.backend_config)
        except StartError as exc:
            print(f"sandbox-broker: {exc}", file=sys.stderr)
            return 1
    if a.cmd == "supervise":
        from .daemon import supervise
        return supervise(a.config, backend_name=a.backend, backend_config=a.backend_config)
    if a.cmd in ("status", "list", "shutdown"):
        from .client import BrokerClient
        from .protocol import BrokerError
        c = BrokerClient(a.socket)
        try:
            if a.cmd == "status":
                out = {"ping": c.ping(), "usage": c.usage()}
            elif a.cmd == "list":
                out = c.list(all=a.all)
            else:
                out = c.shutdown(exit=not a.keep_running)
        except BrokerError as exc:
            print(f"sandbox-broker: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(out, indent=2))
        return 0
    if a.cmd == "audit-summary":
        from .audit import summarize
        print(json.dumps(summarize(a.path), indent=2, default=str))
        return 0
    if a.cmd == "hash-context":
        from .policy import hash_context_dir
        for d in a.dirs:
            print(f"{hash_context_dir(d)}  {d}")
        return 0
    return 2
if __name__ == "__main__":
    sys.exit(main())
