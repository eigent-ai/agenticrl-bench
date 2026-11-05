import json
import random
import sys
from pathlib import Path
run, out = Path(sys.argv[1]), Path(sys.argv[2])
seen, convs = set(), []
for f in sorted((run / "requests").glob("*.jsonl")):
    for line in open(f):
        msgs = json.loads(line)["body"].get("messages")
        if not msgs:
            continue
        key = json.dumps(msgs, sort_keys=True)
        if key not in seen:
            seen.add(key)
            convs.append(msgs)
random.Random(0).shuffle(convs)
convs.sort(key=lambda m: -sum(len(x.get("content") or "") for x in m))
with open(out, "w") as fh:
    for m in convs[:1500]:
        fh.write(json.dumps(m) + "\n")
print(len(convs), "conversations,", min(1500, len(convs)), "kept")
