"""PID-1 guard: refuse signals to a sandbox's PID 1 where the platform would silently ignore them.

On some platforms (Modal's gVisor) a workload's ``kill -9 1`` ends the sandbox; on Linux-kernel platforms the PID-1
of a namespace ignores it (the kernel drops signals to a namespace's init sent from inside that namespace). A tool
that behaves differently per platform must refuse loudly instead (server.py, "Platform conformance"), so where the
platform ignores the signal every workload command starts under a seccomp filter that makes a signal to PID 1 fail
with EPERM (``bash: kill: (1) - Operation not permitted``).

``GUARD_SOURCE`` runs inside the sandbox as ``python3 -I -S -c GUARD_SOURCE <argv...>``: it installs the filter (with
no_new_privs only where the sandbox's root lacks CAP_SYS_ADMIN), then execs argv with the environment the process was
started with (from /proc/self/environ, so Python's own locale handling adds nothing). The filter covers kill, tkill,
tgkill, rt_sigqueueinfo, rt_tgsigqueueinfo with a non-zero signal and pidfd_open, each aimed at PID 1.
"""
from __future__ import annotations

GUARD_SOURCE = r'''
import ctypes, errno, os, struct, sys
argv = sys.argv[1:]
if not argv:
    sys.stderr.write("sandbox-gate: empty command\n"); sys.exit(125)
ARCH = {"x86_64": (0xC000003E, {62: (0, 1), 200: (0, 1), 234: (0, 2), 129: (0, 1), 297: (0, 2), 434: (0, None)}),
        "aarch64": (0xC00000B7, {129: (0, 1), 130: (0, 1), 131: (0, 2), 138: (0, 1), 240: (0, 2), 434: (0, None)})}
machine = os.uname().machine
if machine not in ARCH:
    sys.stderr.write("sandbox-gate: no PID-1 guard for architecture %s\n" % machine); sys.exit(125)
arch, rules = ARCH[machine]
LD, JEQ, RET = 0x20, 0x15, 0x06
ALLOW, DENY = 0x7FFF0000, 0x00050000 | errno.EPERM
code, labels = [], {}
def emit(op, k, jt=0, jf=0): code.append((op, k, jt, jf))
emit(LD, 4); emit(JEQ, arch, 0, "allow"); emit(LD, 0)
for nr, (pid_arg, sig_arg) in sorted(rules.items()):
    nxt = "n%d" % nr
    emit(JEQ, nr, 0, nxt)
    emit(LD, 16 + 8 * pid_arg); emit(JEQ, 1, 0, "allow")
    emit(LD, 20 + 8 * pid_arg); emit(JEQ, 0, 0, "allow")
    if sig_arg is not None:
        emit(LD, 16 + 8 * sig_arg); emit(JEQ, 0, "allow", 0)
    emit(RET, DENY)
    labels[nxt] = len(code); emit(LD, 0)
labels["allow"] = len(code); emit(RET, ALLOW)
raw = b"".join(struct.pack("=HBBI", op, *(t if isinstance(t, int) else labels[t] - i - 1 for t in (jt, jf)), k)
               for i, (op, k, jt, jf) in enumerate(code))
class Prog(ctypes.Structure):
    _fields_ = [("len", ctypes.c_ushort), ("filter", ctypes.c_void_p)]
buf = ctypes.create_string_buffer(raw, len(raw))
prog = Prog(len(code), ctypes.cast(buf, ctypes.c_void_p))
libc = ctypes.CDLL(None, use_errno=True)
prctl = libc.prctl
prctl.argtypes = [ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_ulong]
if prctl(22, 2, ctypes.addressof(prog), 0, 0) != 0:
    if ctypes.get_errno() != errno.EACCES or prctl(38, 1, 0, 0, 0) != 0 or prctl(22, 2, ctypes.addressof(prog), 0, 0) != 0:
        sys.stderr.write("sandbox-gate: cannot install the PID-1 guard (errno %d)\n" % ctypes.get_errno()); sys.exit(125)
try:
    with open("/proc/self/environ", "rb") as f:
        env = dict(kv.split(b"=", 1) for kv in f.read().split(b"\0") if b"=" in kv)
except OSError:
    env = dict(os.environb)
try:
    os.execvpe(argv[0], argv, env)
except FileNotFoundError:
    sys.stderr.write("%s: command not found\n" % argv[0]); sys.exit(127)
except OSError as exc:
    sys.stderr.write("%s: %s\n" % (argv[0], exc.strerror)); sys.exit(126)
'''


def guarded_argv(python: str, argv: list[str]) -> list[str]:
    """``argv`` started under the PID-1 guard by the sandbox's own ``python`` (an absolute path)."""
    return [python, "-I", "-S", "-c", GUARD_SOURCE, *argv]
