#!/usr/bin/env python3
"""Mutual TLS API server."""
import ssl
import socket
import threading


def handle_client(conn):
    try:
        conn.settimeout(10)
        conn.recv(4096)
        conn.send(b"HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\nAuthorized\n")
    except Exception:
        pass
    finally:
        try:
            conn.close()
        except Exception:
            pass


ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain('/etc/tls/server.crt', '/etc/tls/server.key')
ctx.verify_mode = ssl.CERT_REQUIRED
ctx.load_verify_locations('/etc/tls/ca.crt')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 4433))
sock.listen(20)
print("mTLS server listening on 127.0.0.1:4433", flush=True)

with ctx.wrap_socket(sock, server_side=True) as ssock:
    while True:
        try:
            conn, _ = ssock.accept()
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()
        except ssl.SSLError:
            pass
        except Exception as e:
            print(f"Server error: {e}", flush=True)
