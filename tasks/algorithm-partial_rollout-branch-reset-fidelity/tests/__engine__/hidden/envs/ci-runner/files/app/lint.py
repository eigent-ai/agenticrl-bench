import pathlib
import sys

bad = 0
for p in sorted(pathlib.Path(sys.argv[1]).glob("*.py")):
    for i, ln in enumerate(p.read_text().splitlines(), 1):
        if len(ln) > 79 or ln.rstrip() != ln:
            print(f"{p}:{i}: style")
            bad += 1
print(f"{bad} problem(s)")
