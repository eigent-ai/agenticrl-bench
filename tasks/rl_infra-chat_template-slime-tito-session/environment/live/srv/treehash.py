"""Fingerprint of a source tree as it ran: every entry below the root except Python byte-code caches and .git
(regular files by content, symlinks by target, directories and other entries by name; owners and modes are not
part of it). ``python3 -I treehash.py <dir>`` prints it."""
import hashlib
import json
import os
import stat
import sys

SKIP_NAMES = {"__pycache__", ".git"}


def skipped(rel: str) -> bool:
    parts = rel.split("/")
    return any(p in SKIP_NAMES for p in parts) or rel.endswith(".pyc")


def _sha_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def entries(root: str) -> list[list[str]]:
    out = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        rel_dir = os.path.relpath(dirpath, root)
        rel_dir = "" if rel_dir == "." else rel_dir + "/"
        keep = []
        for name in sorted(dirnames + filenames):
            rel = rel_dir + name
            if skipped(rel):
                continue
            p = os.path.join(dirpath, name)
            st = os.lstat(p)
            if stat.S_ISLNK(st.st_mode):
                out.append(["L", rel, os.readlink(p)])
            elif stat.S_ISREG(st.st_mode):
                out.append(["F", rel, _sha_file(p)])
            elif stat.S_ISDIR(st.st_mode):
                out.append(["D", rel, ""])
                keep.append(name)
            else:
                out.append(["O", rel, ""])
        dirnames[:] = [d for d in dirnames if d in keep]
    return sorted(out, key=lambda e: e[1])


def digest(ents: list[list[str]]) -> str:
    return hashlib.sha256(json.dumps(sorted(ents, key=lambda e: e[1]), ensure_ascii=True).encode()).hexdigest()


def tree_hash(root: str) -> str:
    return digest(entries(root))


if __name__ == "__main__":
    print(tree_hash(sys.argv[1]))
