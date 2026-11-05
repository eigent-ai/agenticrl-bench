import json
import os
import numpy as np
VOCAB = 248320
class Rollout:
    def __init__(self, data_dir: str, uid: str, meta: dict):
        self.uid = uid
        self.meta = meta
        z = np.load(os.path.join(data_dir, "rollouts", f"{uid}.npz"), allow_pickle=False)
        self.a = {k: z[k] for k in z.files}
        self.temperature = float(meta["temperature"])
    def call_input_ids(self, k):
        o = self.a["call_in_off"]
        return self.a["call_in_ids"][o[k]:o[k + 1]]
    def call_out(self, k):
        o = self.a["call_out_off"]
        return slice(o[k], o[k + 1])
    def call_support(self, k, j):
        o = self.a["sup_off"]
        r = self.call_out(k).start + j
        return self.a["sup_ids"][o[r]:o[r + 1]], self.a["sup_logp"][o[r]:o[r + 1]]
    def kept(self, r):
        o = self.a["kept_off"]
        return self.a["kept_ids"][o[r]:o[r + 1]], self.a["kept_z"][o[r]:o[r + 1]], self.a["filler"][r]
def load_index(data_dir: str) -> dict:
    with open(os.path.join(data_dir, "rollouts.json")) as f:
        return json.load(f)
def expected_layout(meta: dict, cut: dict | None = None):
    tokens = list(meta["tokens"])
    resp = int(meta["response_length"])
    mask = list(meta["loss_mask"])
    rows = list(meta["row_of_resp"])
    if cut is not None:
        n = int(cut["n_tokens"])
        drop = len(tokens) - n
        if drop > 0:
            tokens = tokens[:n]
            resp -= drop
            mask = mask[:resp]
            rows = rows[:resp]
    return tokens, resp, mask, rows
def zigzag_rows(n: int, cp_size: int, cp_rank: int) -> np.ndarray:
    if cp_size == 1:
        return np.arange(n)
    chunk = (n + 2 * cp_size - 1) // (2 * cp_size)
    idx = np.full(2 * cp_size * chunk, -1, dtype=np.int64)
    idx[:n] = np.arange(n)
    a0, a1 = chunk * cp_rank, chunk * (cp_rank + 1)
    b0, b1 = chunk * (2 * cp_size - cp_rank - 1), chunk * (2 * cp_size - cp_rank)
    return np.concatenate([idx[a0:a1], idx[b0:b1]])
_BASE = None
def noise_row(row: int, width: int, col0: int) -> np.ndarray:
    global _BASE
    if _BASE is None:
        _BASE = np.random.default_rng(20261021).standard_normal(VOCAB).astype(np.float32) * 2.0
    return _BASE[col0:col0 + width] * np.float32(1.0 + 0.05 * (row % 7))
def dense_rows(ro: Rollout, tokens_len: int, rows_needed: np.ndarray, resp_rows: dict, col0: int, width: int):
    out = np.zeros((len(rows_needed), width), dtype=np.float32)
    for i, row in enumerate(rows_needed):
        if row < 0:
            continue
        r = resp_rows.get(int(row))
        if r is None:
            out[i] = noise_row(int(row), width, col0)
            continue
        ids, z, fill = ro.kept(r)
        out[i].fill(fill)
        sel = (ids >= col0) & (ids < col0 + width)
        out[i, ids[sel] - col0] = z[sel]
    return out
