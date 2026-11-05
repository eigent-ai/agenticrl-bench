#!/usr/bin/env python3
"""Set a SHA-512 hash for svcssh, then lock it so shadow shows !$6$..."""
import subprocess

r = subprocess.run(
    ['openssl', 'passwd', '-6', 'DummyLockOnly!'],
    capture_output=True, text=True, check=True,
)
hashed = r.stdout.strip()
subprocess.run(
    ['chpasswd', '-e'],
    input='svcssh:' + hashed + '\n',
    text=True, check=True,
)
print('Set SHA-512 hash for svcssh')
