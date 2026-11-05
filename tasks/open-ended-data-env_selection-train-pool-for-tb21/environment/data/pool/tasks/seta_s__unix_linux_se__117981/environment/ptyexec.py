#!/usr/bin/env python3
"""ptyexec - Run a command inside a PTY environment.

Usage: python3 ptyexec.py <command> [args...]

Executes the given command with its stdin, stdout, and stderr connected
to a pseudo-terminal slave device, so that programs calling isatty()
observe a real terminal.
"""

import fcntl
import os
import select
import struct
import sys
import termios
import tty


def set_winsize(fd, rows, cols):
    """Set the terminal window size on the given file descriptor."""
    winsize = struct.pack('HHHH', rows, cols, 0, 0)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


def copy_loop(master_fd):
    """Read output from master_fd and forward it to stdout until EOF."""
    while True:
        try:
            rlist, _, _ = select.select([master_fd], [], [])
        except (KeyboardInterrupt, InterruptedError):
            continue
        if master_fd in rlist:
            try:
                data = os.read(master_fd, 4096)
            except OSError:
                break
            if not data:
                break
            sys.stdout.buffer.write(data)
            sys.stdout.buffer.flush()


def main():
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <command> [args...]', file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1:]

    master_fd, slave_fd = os.openpty()

    pid = os.fork()

    if pid == 0:
        os.close(master_fd)
        os.dup2(slave_fd, 0)
        os.dup2(slave_fd, 1)
        os.dup2(slave_fd, 2)
        if slave_fd > 2:
            os.close(slave_fd)
        os.execvp(command[0], command)
        sys.exit(127)

    copy_loop(master_fd)
    _, status = os.waitpid(pid, 0)
    exit_code = os.WEXITSTATUS(status) if os.WIFEXITED(status) else 1
    os.close(master_fd)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
