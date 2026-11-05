"""Compare a trained actor's HF export with the base model, tensor by tensor (CPU).
    python compare_actor.py EXPORT_DIR BASE_DIR      -> JSON on stdout
Names are matched after dropping the wrapper prefixes Miles' export and the base checkpoint may differ in; tensors of
the base that the export does not carry (vision tower, MTP) are not compared."""
import json
import sys
from pathlib import Path

import torch
from safetensors import safe_open

PREFIXES = ("model.language_model.", "language_model.model.", "language_model.", "model.")


def canon(name: str) -> str:
    for p in PREFIXES:
        if name.startswith(p):
            return name[len(p):]
    return name


def index(d: Path) -> dict:
    out = {}
    for f in sorted(d.glob("*.safetensors")):
        with safe_open(str(f), "pt") as fh:
            for k in fh.keys():
                out.setdefault(canon(k), (f, k))
    return out


def load(ref):
    f, k = ref
    with safe_open(str(f), "pt") as fh:
        return fh.get_tensor(k)


def main():
    new_dir, base_dir = Path(sys.argv[1]), Path(sys.argv[2])
    new, base = index(new_dir), index(base_dir)
    matched = [k for k in new if k in base]
    changed, compared, max_abs, shape_mismatch = 0, 0, 0.0, 0
    changed_names = []
    for k in matched:
        a, b = load(new[k]), load(base[k])
        if a.shape != b.shape:
            shape_mismatch += 1
            continue
        compared += 1
        if a.dtype != b.dtype:
            a, b = a.float(), b.float()
        if not torch.equal(a, b):
            changed += 1
            max_abs = max(max_abs, float((a.float() - b.float()).abs().max()))
            if len(changed_names) < 20:
                changed_names.append(k)
    print(json.dumps({"export_dir": str(new_dir), "export_tensors": len(new), "base_tensors": len(base),
                      "matched": len(matched), "compared": compared, "shape_mismatch": shape_mismatch,
                      "changed": changed, "max_abs_diff": max_abs, "changed_examples": changed_names,
                      "unmatched_export": sorted(k for k in new if k not in base)[:10]}))


if __name__ == "__main__":
    main()
