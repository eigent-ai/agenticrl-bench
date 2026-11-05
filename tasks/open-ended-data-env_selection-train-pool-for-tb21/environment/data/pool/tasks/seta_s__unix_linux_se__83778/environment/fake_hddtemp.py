#!/usr/bin/env python3
import socket

RESPONSE = b"|/dev/sda|WDC WD6401AALS-00J7B0|31|C||/dev/sdb|WDC WD7501AALS-00J7B0|30|C|"


def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(('', 7634))
    srv.listen(10)
    while True:
        conn, _ = srv.accept()
        try:
            conn.sendall(RESPONSE)
        finally:
            conn.close()


if __name__ == '__main__':
    main()
