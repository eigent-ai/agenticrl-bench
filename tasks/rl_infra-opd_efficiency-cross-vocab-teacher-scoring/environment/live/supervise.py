"""Root service supervisor of the box: becomes a child subreaper, ignores SIGQUIT/SIGHUP, runs the command in its own
process group and waits for it. Every descendant that loses its parent is reparented here instead of to the sandbox's
PID 1 (SGLang signals its parent with SIGQUIT when it dies). SIGTERM / SIGINT stop the whole group.

    supervise.py -- <cmd> [args...]
"""
import ctypes
import os
import signal
import sys
import time

PR_SET_CHILD_SUBREAPER = 36


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    try:
        ctypes.CDLL(None, use_errno=True).prctl(PR_SET_CHILD_SUBREAPER, 1, 0, 0, 0)
    except Exception:  # noqa: BLE001
        pass
    signal.signal(signal.SIGQUIT, signal.SIG_IGN)
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    pid = os.fork()
    if pid == 0:
        os.setpgid(0, 0)
        signal.signal(signal.SIGQUIT, signal.SIG_DFL)
        signal.signal(signal.SIGHUP, signal.SIG_DFL)
        os.execvp(argv[0], argv)
    stop = {"sig": None}

    def on_stop(signum, _frame):
        stop["sig"] = signum
        try:
            os.killpg(pid, signal.SIGTERM)
        except OSError:
            pass

    signal.signal(signal.SIGTERM, on_stop)
    signal.signal(signal.SIGINT, on_stop)
    rc = None
    while True:
        try:
            p, status = os.wait()
        except ChildProcessError:
            break
        except InterruptedError:
            continue
        if p == pid:
            rc = os.waitstatus_to_exitcode(status)
            try:
                os.killpg(pid, signal.SIGKILL)  # whatever the command left in its group
            except OSError:
                pass
    if stop["sig"] is not None:
        time.sleep(0)
    sys.exit(rc if isinstance(rc, int) and rc >= 0 else 1)


if __name__ == "__main__":
    main()
