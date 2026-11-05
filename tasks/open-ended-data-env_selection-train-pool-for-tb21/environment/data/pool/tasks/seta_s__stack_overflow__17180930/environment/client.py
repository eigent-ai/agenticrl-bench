"""Interactive client for the number guessing game."""

import socket
import sys
import threading


def receive_loop(sock):
    buf = b''
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                print('\nDisconnected from server.')
                break
            buf += data
            while b'\n' in buf:
                line, buf = buf.split(b'\n', 1)
                print('<< ' + line.decode('utf-8'))
        except Exception:
            break


def main():
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 7777

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Connected to {}:{}'.format(host, port))

    t = threading.Thread(target=receive_loop, args=(sock,), daemon=True)
    t.start()

    try:
        while True:
            line = input('>> ')
            if not line:
                continue
            sock.send((line + '\n').encode('utf-8'))
            if line.strip().upper() == 'QUIT':
                break
    except (EOFError, KeyboardInterrupt):
        pass
    finally:
        sock.close()


if __name__ == '__main__':
    main()
