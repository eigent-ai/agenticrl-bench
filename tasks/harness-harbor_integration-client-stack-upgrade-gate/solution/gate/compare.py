import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "rig"))
from engine_diff import episode_diff, load, outcome
def live_views(reqs, records):
    out = []
    for r in reqs:
        e = r.get("engine") or {}
        rec = records.get(e.get("rid")) or {}
        body = r["body"] if isinstance(r.get("body"), dict) else {}
        out.append({"status": e.get("status"), "prompt": rec.get("ids") or e.get("ids"), "sampling": rec.get("sampling"),
                    "max_tokens": body.get("max_completion_tokens", body.get("max_tokens"))})
    return out
def live_episode_diff(A, B, oa, ob, records):
    reasons = []
    if outcome(oa) != outcome(ob):
        reasons.append(f"outcome {outcome(oa)} -> {outcome(ob)}")
    if len(A) != len(B):
        reasons.append(f"requests {len(A)} -> {len(B)}")
    for i, (x, y) in enumerate(zip(live_views(A, records), live_views(B, records))):
        if x["prompt"] is None or y["prompt"] is None:
            reasons.append(f"no server record @{i} (status {x['status']} / {y['status']})")
            break
        diff = [k for k in ("status", "prompt", "sampling", "max_tokens") if x[k] != y[k]]
        if diff:
            k = diff[0]
            if k == "sampling":
                sx, sy = x[k] or {}, y[k] or {}
                reasons.append(f"sampling@{i} { {s: (sx.get(s), sy.get(s)) for s in set(sx) | set(sy) if sx.get(s) != sy.get(s)} }")
            else:
                reasons.append(f"{k}@{i}")
            break
    return reasons
def main():
    battery, ref, cand, tok_ref, tok_cand = sys.argv[1:6]
    records = None
    if "--engine" in sys.argv:
        records = json.loads(Path(sys.argv[sys.argv.index("--engine") + 1]).read_text())
    ra, oa = load(ref)
    rb, ob = load(cand)
    bad = {}
    for ep in sorted(set(oa) | set(ob)):
        if records is None:
            r = episode_diff(battery, ep, ra.get(ep, []), rb.get(ep, []), oa.get(ep), ob.get(ep))
        else:
            r = live_episode_diff(ra.get(ep, []), rb.get(ep, []), oa.get(ep), ob.get(ep), records)
        if r:
            bad[ep] = r
    ta = Path(tok_ref).read_text().split()
    tb = Path(tok_cand).read_text().split() if Path(tok_cand).exists() else []
    tok_diff = [i for i, (x, y) in enumerate(zip(ta, tb)) if x != y] + ([-1] if len(ta) != len(tb) else [])
    fams = {}
    for ep in bad:
        fams.setdefault(ep.split("__")[0], []).append(ep)
    for f, eps in sorted(fams.items()):
        print(f"  {f}: {len(eps)} trial(s) differ, e.g. {eps[0]}: {bad[eps[0]][:2]}")
    if tok_diff:
        print(f"  token counting differs on {len(tok_diff)} of {len(ta)} probe conversations "
              f"(summarization/unwinding points move near the context budget)")
    where = "as SGLang recorded them" if records is not None else "as the server and the trainer see them"
    if bad or tok_diff:
        print(f"UNSAFE: {len(bad)} of {len(oa)} replayed trials change what the server or the trainer gets ({where})")
        sys.exit(1)
    print(f"SAFE: all {len(oa)} replayed trials identical {where}")
    sys.exit(0)
if __name__ == "__main__":
    main()
