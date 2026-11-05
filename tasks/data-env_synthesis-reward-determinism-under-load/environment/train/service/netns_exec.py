"""Start a service process: bring up loopback (the service runs in its own network namespace), drop to the service
user, exec the command.   netns_exec.py [--user rlchk] -- <cmd> [args...]    |    netns_exec.py --probe
Users: rlsvc (GPU jobs; group rlgpu) or rlchk (`rl check`; no GPUs; group rlsvc to read the task store)."""
import fcntl
import grp
import os
import pwd
import socket
import struct
import sys

SIOCGIFFLAGS, SIOCSIFFLAGS, IFF_UP, IFF_RUNNING = 0x8913, 0x8914, 0x1, 0x40


def lo_up():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        ifr = struct.pack("16sH14x", b"lo", 0)
        flags = struct.unpack("16sH14x", fcntl.ioctl(s, SIOCGIFFLAGS, ifr))[1]
        if not flags & IFF_UP:
            fcntl.ioctl(s, SIOCSIFFLAGS, struct.pack("16sH14x", b"lo", flags | IFF_UP | IFF_RUNNING))
    finally:
        s.close()


def probe():
    lo_up()
    srv = socket.socket()
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    c = socket.create_connection(srv.getsockname(), timeout=5)
    c.close()
    srv.close()
    print("probe-ok")


def main():
    if sys.argv[1:2] == ["--probe"]:
        probe()
        return
    i = sys.argv.index("--")
    head, argv = sys.argv[1:i], sys.argv[i + 1:]
    name = head[head.index("--user") + 1] if "--user" in head else "rlsvc"
    groups = {"rlsvc": ["rlgpu"], "rlchk": ["rlsvc"]}[name]
    try:
        lo_up()
    except OSError:
        pass
    u = pwd.getpwnam(name)
    os.setgroups([grp.getgrnam(g).gr_gid for g in groups])
    os.setgid(u.pw_gid)
    os.setuid(u.pw_uid)
    os.umask(0o022)
    os.execvpe(argv[0], argv, os.environ)


if __name__ == "__main__":
    main()
