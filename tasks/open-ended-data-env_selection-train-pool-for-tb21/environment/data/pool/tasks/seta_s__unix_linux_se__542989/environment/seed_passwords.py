#!/usr/bin/env python3
"""Seed MD5 password hashes for alice, bob, charlie, and svcapp."""
import subprocess

users = [
    ('alice',   'Password123!'),
    ('bob',     'SecurePass456!'),
    ('charlie', 'MyPass789!'),
    ('svcapp',  'TempSvcPass!'),
]

for username, password in users:
    r = subprocess.run(
        ['openssl', 'passwd', '-1', password],
        capture_output=True, text=True, check=True,
    )
    hashed = r.stdout.strip()
    subprocess.run(
        ['chpasswd', '-e'],
        input=username + ':' + hashed + '\n',
        text=True, check=True,
    )
    print(f'Seeded MD5 hash for {username}')
