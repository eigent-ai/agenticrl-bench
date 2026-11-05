from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
EXIT_TIMEOUT = 124
EXIT_GATE = 125
_HIDDEN_KEYS = {"backend", "backend_error", "pid", "euid"}
def _policy_hints() -> dict[str, Any]:
    try:
        from .policy import load_policy
        p = load_policy(strict=False)
    except Exception:
        return {}
    L = p.limits
    return {"cpu": f"default {L.default_cpu:g}, allowed {L.min_cpu:g}-{L.max_cpu:g}",
            "memory": f"default {L.default_memory_mb}, allowed {L.min_memory_mb}-{L.max_memory_mb}",
            "timeout": f"default {L.default_timeout_s}, max {L.max_timeout_s}",
            "idle": f"default {L.idle_timeout_s or 'none'}, max {L.max_idle_timeout_s}",
            "exec": f"default {L.default_exec_timeout_s}, max {L.max_exec_timeout_s}",
            "file": f"max {L.max_file_bytes} bytes",
            "images": ", ".join(p.images.allow) or "none (build contexts only)",
            "contexts": ("any" if p.images.allow_any_build_context else
                         f"{len(p.images.build_contexts)} registered context hash(es)"),
            "network": "none" if p.sandbox.network == "none" else "outbound allowed",
            "concurrent": str(L.max_concurrent)}
def _kv(items: list[str] | None, what: str) -> dict[str, str] | None:
    if not items:
        return None
    out = {}
    for item in items:
        key, sep, value = item.partition("=")
        if not sep or not key:
            raise SystemExit(f"sandbox: {what} must be KEY=VALUE, got {item!r}")
        out[key] = value
    return out
def _clean(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _clean(v) for k, v in obj.items() if k not in _HIDDEN_KEYS}
    if isinstance(obj, list):
        return [_clean(v) for v in obj]
    return obj
def _print(obj: Any) -> None:
    print(json.dumps(_clean(obj), indent=2, sort_keys=True, default=str))
def _command(argv: list[str]) -> list[str]:
    if not argv:
        raise SystemExit("sandbox: missing command (put it after --)")
    return argv
def build_parser() -> argparse.ArgumentParser:
    h = _policy_hints()
    def hint(key: str, fallback: str = "see `sandbox limits`") -> str:
        return h.get(key, fallback)
    p = argparse.ArgumentParser(
        prog="sandbox",
        description="Create and drive isolated task sandboxes through the local sandbox service.",
        epilog=((f"Sandbox network: {h['network']}. Images: {h['images']}; build contexts: {h['contexts']}. "
                 f"At most {h['concurrent']} sandboxes at once. " if h else
                 "Run `sandbox limits` for the effective limits, images and network policy. ") +
                "Run `sandbox <command> --help` for details."),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--socket", help="service socket (default: $SANDBOX_GATE_SOCKET or /run/sandbox-broker.sock)")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    sub = p.add_subparsers(dest="cmd", required=True, metavar="COMMAND")
    sub.add_parser("status", help="service readiness, live sandboxes and remaining budget")
    sub.add_parser("limits", help="effective limits, allowed images and network policy")
    s = sub.add_parser("list", help="list your sandboxes")
    s.add_argument("--all", action="store_true", help="every user's sandboxes (administrators only)")
    def image_opts(s: argparse.ArgumentParser) -> None:
        g = s.add_mutually_exclusive_group(required=True)
        g.add_argument("--image", metavar="REF", help=f"registry image; allowed: {hint('images')}")
        g.add_argument("--context", metavar="DIR",
                       help=f"Docker build context (Dockerfile at its root); allowed: {hint('contexts')}")
        s.add_argument("--cpu", type=float, metavar="CORES", help=f"CPU cores ({hint('cpu')})")
        s.add_argument("--memory-mb", type=int, metavar="MIB", help=f"memory in MiB ({hint('memory')})")
        s.add_argument("--timeout", type=int, metavar="SECONDS", help=f"sandbox lifetime ({hint('timeout')})")
        s.add_argument("--idle-timeout", type=int, metavar="SECONDS",
                       help=f"stop after this long without activity ({hint('idle')})")
        s.add_argument("--workdir", metavar="PATH", help="default working directory (absolute)")
        s.add_argument("--env", action="append", metavar="KEY=VALUE", help="environment variable (repeatable)")
        s.add_argument("--label", action="append", metavar="KEY=VALUE",
                       help="label shown by `sandbox list` (repeatable, at most 16)")
    s = sub.add_parser("create", help="create a sandbox and print its id")
    image_opts(s)
    s = sub.add_parser("exec", help="run a command in a sandbox, streaming its output",
                       description="Run CMD (no shell; use `-- sh -c '...'` for one) and exit with its status.")
    s.add_argument("id")
    s.add_argument("--timeout", type=int, metavar="SECONDS", help=f"command timeout ({hint('exec')})")
    s.add_argument("--workdir", metavar="PATH", help="working directory (absolute)")
    s.add_argument("--env", action="append", metavar="KEY=VALUE", help="environment variable (repeatable)")
    s.add_argument("--stdin", action="store_true", help="send this command's standard input to CMD")
    s.add_argument("argv", nargs="*", metavar="CMD", help="command and its arguments, after --")
    s = sub.add_parser("run", help="create a sandbox, run one command, terminate it",
                       description="Create a sandbox, run CMD in it, terminate it (unless --keep) and exit "
                                   "with CMD's status.")
    image_opts(s)
    s.add_argument("--exec-timeout", type=int, metavar="SECONDS", help=f"command timeout ({hint('exec')})")
    s.add_argument("--stdin", action="store_true", help="send this command's standard input to CMD")
    s.add_argument("--keep", action="store_true", help="keep the sandbox and print its id on stderr")
    s.add_argument("argv", nargs="*", metavar="CMD", help="command and its arguments, after --")
    s = sub.add_parser("put", help="copy a local file or directory into a sandbox")
    s.add_argument("id")
    s.add_argument("local")
    s.add_argument("remote", help="absolute path in the sandbox")
    s.add_argument("--mode", metavar="OCTAL", help="file mode, e.g. 0755 (files only)")
    s = sub.add_parser("get", help=f"copy a file (or with -r a directory) out of a sandbox ({hint('file')})")
    s.add_argument("id")
    s.add_argument("remote", help="absolute path in the sandbox")
    s.add_argument("local")
    s.add_argument("-r", "--recursive", action="store_true", help="REMOTE is a directory")
    s = sub.add_parser("poll", help="is the sandbox still running (else its exit code)")
    s.add_argument("id")
    s = sub.add_parser("terminate", help="stop sandboxes and release their resources")
    s.add_argument("ids", nargs="+", metavar="id")
    return p
def _create_kwargs(a: argparse.Namespace) -> dict[str, Any]:
    kw: dict[str, Any] = {"cpu": a.cpu, "memory_mb": a.memory_mb, "timeout_s": a.timeout,
                          "idle_timeout_s": a.idle_timeout, "workdir": a.workdir,
                          "env": _kv(a.env, "--env"), "labels": _kv(a.label, "--label")}
    if a.image:
        kw["image"] = a.image
    else:
        kw["build_context"] = a.context
    return kw
def _exec(sb, argv: list[str], timeout: int | None, workdir: str | None, env: dict | None, use_stdin: bool) -> int:
    def out(fd: str, data: bytes) -> None:
        stream = sys.stdout.buffer if fd == "stdout" else sys.stderr.buffer
        stream.write(data)
        stream.flush()
    stdin = sys.stdin.buffer.read() if use_stdin else None
    r = sb.exec(*argv, timeout=timeout, workdir=workdir, env=env, stdin=stdin, binary=True, on_output=out)
    if r.stdout_truncated or r.stderr_truncated:
        print("sandbox: output was truncated at the size limit", file=sys.stderr)
    if r.timed_out:
        print("sandbox: command timed out", file=sys.stderr)
        return EXIT_TIMEOUT
    return r.returncode if 0 <= r.returncode <= 255 else 1
def main(argv: list[str] | None = None) -> int:
    from .client import BrokerClient
    from .protocol import BrokerError
    argv = list(sys.argv[1:] if argv is None else argv)
    tail: list[str] | None = None
    if "--" in argv:
        i = argv.index("--")
        argv, tail = argv[:i], argv[i + 1:]
    a = build_parser().parse_args(argv)
    if tail is not None and hasattr(a, "argv"):
        a.argv = list(a.argv) + tail
    c = BrokerClient(a.socket)
    try:
        if a.cmd == "status":
            ping = c.ping()
            out = {"ready": bool(ping.get("ready")), "version": ping.get("version"), "usage": c.usage()}
            if ping.get("backend_error"):
                out["state"] = "unavailable"
            _print(out)
        elif a.cmd == "limits":
            _print(c.policy())
        elif a.cmd == "list":
            rows = c.list(all=a.all)
            if a.json:
                _print(rows)
            else:
                for r in rows:
                    state = "running" if r.get("running") else f"ended ({r.get('end_reason')})"
                    print(f"{r['id']}  {state:<20} {r.get('image', '?')}  cpu={r.get('cpu')} "
                          f"mem={r.get('memory_mb')}MiB  {json.dumps(r.get('labels') or {})}")
        elif a.cmd == "create":
            sb = c.create(**_create_kwargs(a))
            _print({"id": sb.id, **sb.info}) if a.json else print(sb.id)
        elif a.cmd == "exec":
            return _exec(c.sandbox(a.id), _command(a.argv), a.timeout, a.workdir, _kv(a.env, "--env"), a.stdin)
        elif a.cmd == "run":
            cmd = _command(a.argv)
            sb = c.create(**_create_kwargs(a))
            try:
                return _exec(sb, cmd, a.exec_timeout, None, None, a.stdin)
            finally:
                if a.keep:
                    print(f"sandbox: kept {sb.id}", file=sys.stderr)
                else:
                    sb.terminate()
        elif a.cmd == "put":
            sb = c.sandbox(a.id)
            if os.path.isdir(a.local):
                sb.upload_dir(a.local, a.remote)
            else:
                sb.put_file(a.remote, Path(a.local), mode=int(a.mode, 8) if a.mode else None)
        elif a.cmd == "get":
            sb = c.sandbox(a.id)
            if a.recursive:
                sb.download_dir(a.remote, a.local)
            else:
                target = Path(a.local)
                if target.is_dir():
                    target = target / os.path.basename(a.remote)
                target.write_bytes(sb.get_file(a.remote))
        elif a.cmd == "poll":
            rc = c.sandbox(a.id).poll()
            _print({"id": a.id, "running": rc is None, "exit_code": rc}) if a.json else \
                print("running" if rc is None else f"exited {rc}")
        elif a.cmd == "terminate":
            for sid in a.ids:
                c.sandbox(sid).terminate()
        return 0
    except BrokerError as exc:
        print(f"sandbox: error [{exc.kind}]: {exc}", file=sys.stderr)
        return EXIT_GATE
    except (TimeoutError, RuntimeError, OSError, ValueError) as exc:
        print(f"sandbox: {exc}", file=sys.stderr)
        return EXIT_GATE
if __name__ == "__main__":
    sys.exit(main())
