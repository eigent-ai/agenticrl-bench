import hashlib
import json
import os
import sys
from pathlib import Path
def files(d):
    out = {}
    for p in Path(d).rglob("*"):
        if p.is_file() and not p.is_symlink():
            st = p.stat()
            out[f"{st.st_dev}:{st.st_ino}"] = [str(p), st.st_size]
    return out
def events(d, snap):
    for key, (p, size) in files(d).items():
        start = snap.get(key, [None, 0])[1]
        if size <= start:
            continue
        with open(p, "rb") as f:
            f.seek(start)
            for raw in f:
                if b'"request.received"' not in raw[:200] and b'"request.finished"' not in raw[:200]:
                    continue
                i = raw.find(b"{")
                try:
                    yield json.loads(raw[i:])
                except ValueError:
                    continue
def collect(d, snap):
    rec = {}
    for e in events(d, snap):
        rid = e.get("rid")
        if not isinstance(rid, str) or rid.startswith("HEALTH_CHECK"):
            continue
        r = rec.setdefault(rid, {})
        if e.get("event") == "request.received":
            sp = dict((e.get("obj") or {}).get("sampling_params") or {})
            sp.pop("max_new_tokens", None)
            r["sampling"] = sp
        else:
            ids = (e.get("out") or {}).get("prompt_token_ids")
            if isinstance(ids, list):
                r["ids"] = hashlib.sha256(",".join(map(str, ids)).encode()).hexdigest()
    return rec
def main():
    cmd = sys.argv[1]
    if cmd == "snapshot":
        Path(sys.argv[3]).write_text(json.dumps(files(sys.argv[2])))
    elif cmd == "collect":
        snap = json.loads(Path(sys.argv[3]).read_text())
        Path(sys.argv[4]).write_text(json.dumps(collect(sys.argv[2], snap)))
    elif cmd == "report":
        rec = json.loads(Path(sys.argv[2]).read_text())
        hashes = [r["ids"] for r in rec.values() if r.get("ids")]
        tmp = sys.argv[3] + ".tmp"
        with open(tmp, "w") as f:
            json.dump({"prompt_ids_sha256": hashes}, f)
        os.replace(tmp, sys.argv[3])
    else:
        sys.exit(f"unknown command {cmd}")
if __name__ == "__main__":
    main()
