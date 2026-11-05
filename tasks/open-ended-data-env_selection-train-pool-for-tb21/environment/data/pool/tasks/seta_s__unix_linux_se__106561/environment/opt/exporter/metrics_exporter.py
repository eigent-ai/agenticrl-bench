#!/usr/bin/env python3
"""Metrics exporter service."""
import socket, time

HOST = '0.0.0.0'
PORT = 9000

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind((HOST, PORT))
srv.listen(5)
while True:
    time.sleep(30)
