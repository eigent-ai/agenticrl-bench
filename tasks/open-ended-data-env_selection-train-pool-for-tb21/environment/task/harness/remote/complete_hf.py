"""Complete a saved HF checkpoint with the base model's tensors it lacks (inbox-rl-v1; rld runs it as root after a
training job, with /opt/sglang/bin/python for safetensors).

Miles exports only what the Megatron model trains: Qwen3.5's language model (+ lm_head). The base checkpoint
(Qwen3_5ForConditionalGeneration) also has the vision tower and the MTP head. Those tensors are copied unchanged from
the base into model-base-extra.safetensors and added to the checkpoint's index, so the directory is a complete HF model
for SGLang, for `rl train --from` and for a shipped release.

    python complete_hf.py CKPT_DIR [--base /models/Qwen3.5-4B]      (idempotent; marker .base_completed)
"""
import argparse
import json
from pathlib import Path

from safetensors import safe_open
from safetensors.torch import save_file

EXTRA_PREFIXES = ("model.visual.", "visual.", "mtp.")


def weight_map(d: Path) -> dict:
    idx = d / "model.safetensors.index.json"
    if idx.exists():
        return json.loads(idx.read_text())["weight_map"]
    out = {}
    for f in sorted(d.glob("*.safetensors")):
        with safe_open(str(f), "pt") as s:
            out.update({k: f.name for k in s.keys()})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ckpt")
    ap.add_argument("--base", default="/models/Qwen3.5-4B")
    a = ap.parse_args()
    d, base = Path(a.ckpt), Path(a.base)
    if (d / ".base_completed").exists():
        print(json.dumps({"ckpt": str(d), "already": True}))
        return
    have, bmap = weight_map(d), weight_map(base)
    absent = sorted(set(bmap) - set(have))
    # only whole modules the export never has; anything else absent is reported, never filled from the base (a
    # naming mismatch must not put base weights next to trained ones)
    missing = [k for k in absent if k.startswith(EXTRA_PREFIXES)]
    other = [k for k in absent if not k.startswith(EXTRA_PREFIXES)]
    added = 0
    if missing:
        tensors = {}
        by_file = {}
        for k in missing:
            by_file.setdefault(bmap[k], []).append(k)
        for fn, keys in by_file.items():
            with safe_open(str(base / fn), "pt") as s:
                for k in keys:
                    tensors[k] = s.get_tensor(k).contiguous()
        save_file(tensors, str(d / "model-base-extra.safetensors"), metadata={"format": "pt"})
        added = len(tensors)
        idx = d / "model.safetensors.index.json"
        if idx.exists():
            index = json.loads(idx.read_text())
        else:
            index = {"metadata": {}, "weight_map": dict(have)}
        index["weight_map"].update({k: "model-base-extra.safetensors" for k in tensors})
        index.setdefault("metadata", {})["total_size"] = int(index["metadata"].get("total_size", 0)) + sum(
            t.numel() * t.element_size() for t in tensors.values())
        idx.write_text(json.dumps(index, indent=2))
    rep = {"added_from_base": added, "absent_not_filled": len(other), "absent_examples": other[:5]}
    (d / ".base_completed").write_text(json.dumps(rep))
    print(json.dumps({"ckpt": str(d), **rep, "added_examples": missing[:3]}))


if __name__ == "__main__":
    main()
