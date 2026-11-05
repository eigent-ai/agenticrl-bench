import sys

for i in range(1, 5001):
    t = i - 1
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    level = "ERROR" if i % 100 == 0 else ("WARN" if i % 50 == 0 else "INFO")
    print(f"2024-01-15 {h:02d}:{m:02d}:{s:02d} {level} ENTRY_{i:05d} [app.service] Line {i}")
