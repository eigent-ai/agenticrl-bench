line = b'A' * 49 + b'\n'  # exactly 50 bytes per line
with open('/var/log/app/app.log', 'wb') as f:
    for _ in range(4096):  # 4096 * 50 = 204,800 bytes
        f.write(line)
