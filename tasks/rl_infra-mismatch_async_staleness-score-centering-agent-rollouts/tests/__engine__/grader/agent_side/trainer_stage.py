import argparse
import json
import os
import pickle
import sys
import time
import traceback
from datetime import timedelta
from unittest.mock import patch
import numpy as np
ap = argparse.ArgumentParser()
ap.add_argument("--cases", required=True)
ap.add_argument("--data", required=True)
ap.add_argument("--rollout-out", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--only", default=None)
a = ap.parse_args()
from common import VOCAB, Rollout, expected_layout, load_index, zigzag_rows, dense_rows
CASES = json.load(open(a.cases))
INDEX = load_index(a.data)
class _DumperStub:
    def wrap_forward_step(self, f):
        return f
def _patch_cuda(torch):
    torch.cuda.current_device = lambda: "cpu"
    torch.Tensor.cuda = lambda self, *args, **kwargs: self
    torch.cuda.synchronize = lambda *args, **kwargs: None
    torch.cuda.get_device_capability = lambda *args, **kwargs: (9, 0)
    try:
        import megatron.training.arguments as mta
        import megatron.training.utils.common_utils as mcu
        mta.get_device_arch_version = lambda: 9
        mcu.get_device_arch_version = lambda: 9
    except Exception:
        pass
def _worker(rank, world, tp, cp, dp, case, rendezvous, out_dir, err_path):
    import torch
    import torch.distributed as dist
    torch.set_num_threads(max(1, 8 // world))
    os.environ["CUDA_DEVICE_MAX_CONNECTIONS"] = "1"
    _patch_cuda(torch)
    try:
        dist.init_process_group("gloo", init_method=rendezvous, rank=rank, world_size=world,
                                timeout=timedelta(seconds=600))
        tp_rank, cp_rank = rank % tp, rank // tp
        from miles.backends.training_utils import parallel as par
        tp_groups = [dist.new_group([c * tp + t for t in range(tp)]) for c in range(cp)]
        cp_groups = [dist.new_group([c * tp + t for c in range(cp)]) for t in range(tp)]
        single = par.GroupInfo(rank=0, size=1, group=None)
        tp_info = par.GroupInfo(rank=tp_rank, size=tp, group=tp_groups[cp_rank] if tp > 1 else None)
        cp_info = par.GroupInfo(rank=cp_rank, size=cp, group=cp_groups[tp_rank] if cp > 1 else None)
        state = {n: single for n in ("intra_dp", "intra_dp_cp", "pp", "ep", "etp", "indep_dp")}
        if cp > 1:
            state["intra_dp_cp"] = par.GroupInfo(rank=cp_rank, size=cp, group=cp_groups[tp_rank])
        par.set_parallel_state(par.ParallelState(**state, tp=tp_info, cp=cp_info))
        try:
            from megatron.core import parallel_state as mpu
            mpu.get_tensor_model_parallel_group = lambda *x, **k: tp_info.group
            mpu.get_tensor_model_parallel_rank = lambda *x, **k: tp_rank
            mpu.get_tensor_model_parallel_world_size = lambda *x, **k: tp
            mpu.get_context_parallel_group = lambda *x, **k: cp_info.group
            mpu.get_context_parallel_rank = lambda *x, **k: cp_rank
            mpu.get_context_parallel_world_size = lambda *x, **k: cp
            mpu.get_data_parallel_rank = lambda *x, **k: 0
            mpu.get_data_parallel_world_size = lambda *x, **k: 1
        except Exception:
            pass
        from argv import build_argv
        from miles.utils.arguments import parse_args
        with patch("sys.argv", ["train.py"] + build_argv(case, tp=tp, cp=cp)):
            args = parse_args()
        if getattr(args, "padded_vocab_size", None) is None:
            args.padded_vocab_size = VOCAB
        args.rank, args.local_rank = rank, rank
        from miles.backends.megatron_utils import model as model_mod
        from miles.backends.training_utils.data import rollout as rollout_mod
        from miles.backends.training_utils.loss.objective import compute_advantages_and_returns
        from miles.ray.rollout.train_data_conversion import process_rollout_data_shard, split_train_data_by_dp_raw
        with open(os.path.join(a.rollout_out, case["rollout_case"], "train_data.pkl"), "rb") as f:
            train_data_all = pickle.load(f)
        width = VOCAB // tp
        col0 = tp_rank * width
        cache = {}
        def ro_of(uid):
            if uid not in cache:
                cache[uid] = Rollout(a.data, uid, INDEX[uid])
            return cache[uid]
        expected = {}
        for uid in [u for g in case["groups"] for u in g]:
            toks, resp, mask, rows = expected_layout(INDEX[uid], case.get("cuts", {}).get(uid))
            expected[tuple(toks)] = (uid, resp, mask, rows)
        acc = {"uids": [], "rows": [], "koff": [0], "kid": [], "kval": [], "tsum": [], "tsq": [], "ntail": [],
               "other": {}, "pad": 0.0, "loss": []}
        mbs = int(case.get("micro_batch_size", 1))
        for dp_rank in range(dp):
            data = pickle.loads(pickle.dumps(train_data_all))
            shard = split_train_data_by_dp_raw(args, data, dp_size=dp)[dp_rank]
            shard = process_rollout_data_shard(args, shard)
            with patch.object(rollout_mod, "process_rollout_data", lambda *x, **k: (shard, None)):
                rollout_data, _ = rollout_mod.get_rollout_data(args, None)
            compute_advantages_and_returns(args, rollout_data)
            n_samples = len(rollout_data["tokens"])
            mb_indices = [list(range(i, min(i + mbs, n_samples))) for i in range(0, n_samples, mbs)]
            iterator = rollout_mod.DataIterator(rollout_data, micro_batch_indices=mb_indices)
            plan_all = []
            for t in rollout_data["tokens"]:
                key = tuple(int(x) for x in (t.tolist() if hasattr(t, "tolist") else t))
                if key not in expected:
                    raise RuntimeError("a training sample's tokens do not match any replayed rollout")
                uid, resp, mask, rows = expected[key]
                L = len(key)
                P = L - resp
                local = zigzag_rows(L, cp, cp_rank)
                trained = {}
                for i in range(resp):
                    if mask[i] == 1 and rows[i] >= 0:
                        trained[P + i - 1] = rows[i]
                toks = np.where(local >= 0, np.asarray(key)[np.maximum(local, 0)], 0)
                plan_all.append((uid, local, trained, toks))
            box = {}
            class FakeModel:
                def __call__(self, input_ids=None, fp32_output=True, **kwargs):
                    plan = [plan_all[i] for i in box["cur"]]
                    T = input_ids.shape[-1]
                    got = input_ids.reshape(-1).numpy()
                    flat = np.concatenate([p[3] for p in plan])
                    if len(flat) > T or not np.array_equal(got[: len(flat)], flat):
                        raise RuntimeError("get_batch token layout differs from the zigzag/thd layout")
                    parts = [dense_rows(ro_of(uid), 0, local, trained, col0, width) for uid, local, trained, _ in plan]
                    x = np.concatenate(parts)
                    if T > len(x):
                        x = np.concatenate([x, np.zeros((T - len(x), width), np.float32)])
                    leaf = torch.from_numpy(x).unsqueeze(0).requires_grad_(True)
                    box["leaf"] = leaf
                    box["plan"] = plan
                    return leaf
            def summarise(g, plan):
                pos = 0
                for uid, local, trained, _ in plan:
                    ro = ro_of(uid)
                    other = 0.0
                    for li, row in enumerate(local):
                        gi = g[pos + li]
                        r = trained.get(int(row)) if row >= 0 else None
                        if r is None:
                            other += float(gi @ gi)
                            continue
                        ids, _, _ = ro.kept(r)
                        sel = (ids >= col0) & (ids < col0 + width)
                        cols = ids[sel] - col0
                        vals = gi[cols]
                        acc["uids"].append(uid)
                        acc["rows"].append(r)
                        acc["kid"].extend(ids[sel].tolist())
                        acc["kval"].extend(vals.tolist())
                        acc["koff"].append(len(acc["kid"]))
                        tl = np.delete(gi, cols).astype(np.float64)
                        acc["tsum"].append(float(tl.sum()))
                        acc["tsq"].append(float(tl @ tl))
                        acc["ntail"].append(width - int(sel.sum()))
                    acc["other"][uid] = acc["other"].get(uid, 0.0) + other
                    pos += len(local)
                acc["pad"] += float((g[pos:] * g[pos:]).sum())
            def fake_fbf(forward_step_func, data_iterator, model, num_microbatches, **kwargs):
                di = data_iterator[0] if isinstance(data_iterator, list) else data_iterator
                m = model[0] if isinstance(model, list) else model
                logs = []
                for k in range(num_microbatches):
                    box["cur"] = mb_indices[k]
                    out, loss_func = forward_step_func(di, m)
                    loss, _, log = loss_func(out)
                    if not torch.isfinite(loss).all():
                        raise RuntimeError(f"non-finite loss {loss}")
                    loss.backward()
                    grad = box["leaf"].grad
                    if grad is None:
                        raise RuntimeError("no gradient reached the logits")
                    g = grad[0].double().numpy()
                    if not np.isfinite(g).all():
                        raise RuntimeError("non-finite gradient")
                    summarise(g, box["plan"])
                    acc["loss"].append(float(loss.detach()))
                    box.pop("leaf")
                    logs.append(log)
                return logs
            num_rollouts = len(set(int(x) for x in rollout_data.get("rollout_ids", range(n_samples))))
            with patch.object(model_mod, "get_forward_backward_func", lambda *x, **k: fake_fbf), \
                    patch.object(model_mod, "get_packed_seq_params", lambda *x, **k: None, create=True):
                model_mod.run_forward_backward_pass(args, _DumperStub(), [iterator], [FakeModel()], len(mb_indices),
                                                    num_rollouts, forward_only=False)
        np.savez(
            os.path.join(out_dir, f"tp{tp_rank}_cp{cp_rank}.npz"),
            uids=np.array(acc["uids"]), rows=np.array(acc["rows"], dtype=np.int64),
            koff=np.array(acc["koff"], dtype=np.int64), kid=np.array(acc["kid"], dtype=np.int64),
            kval=np.array(acc["kval"], dtype=np.float64), tsum=np.array(acc["tsum"], dtype=np.float64),
            tsq=np.array(acc["tsq"], dtype=np.float64), ntail=np.array(acc["ntail"], dtype=np.int64),
            other_uids=np.array(list(acc["other"])),
            other_sq=np.array([acc["other"][u] for u in acc["other"]], dtype=np.float64),
            pad_sq=np.array([acc["pad"]]), loss=np.array(acc["loss"] or [np.nan]),
        )
        dist.barrier()
    except BaseException:
        with open(err_path + f".{rank}", "w") as f:
            f.write(traceback.format_exc()[-8000:])
        raise
    finally:
        if dist.is_initialized():
            dist.destroy_process_group()
def main():
    import torch.multiprocessing as mp
    status = {}
    for case in CASES:
        for layout in case["layouts"]:
            tp, cp, dp = layout
            key = f"{case['id']}@tp{tp}cp{cp}dp{dp}"
            if a.only and not key.startswith(a.only):
                continue
            out_dir = os.path.join(a.out, key)
            os.makedirs(out_dir, exist_ok=True)
            t0 = time.time()
            rstat = json.load(open(os.path.join(a.rollout_out, "rollout_status.json")))
            if not rstat.get(case["rollout_case"], {}).get("ok"):
                status[key] = {"ok": False, "error": "rollout stage failed for this case"}
                continue
            err = os.path.join(out_dir, "error")
            rdzv = os.path.join(out_dir, "rdzv")
            for stale in [rdzv, *[err + f".{r}" for r in range(tp * cp)]]:
                if os.path.exists(stale):
                    os.remove(stale)
            rendezvous = "file://" + rdzv
            try:
                mp.spawn(_worker, args=(tp * cp, tp, cp, dp, case, rendezvous, out_dir, err), nprocs=tp * cp,
                         join=True)
                status[key] = {"ok": True, "s": round(time.time() - t0, 1)}
            except BaseException as e:
                tb = ""
                for r in range(tp * cp):
                    if os.path.exists(err + f".{r}"):
                        tb = open(err + f".{r}").read()
                        break
                status[key] = {"ok": False, "s": round(time.time() - t0, 1), "error": f"{type(e).__name__}: {e}"[:1000],
                               "tb": tb[-6000:]}
            print(json.dumps({key: {k: v for k, v in status[key].items() if k != "tb"}}), flush=True)
            with open(os.path.join(a.out, "trainer_status.json"), "w") as f:
                json.dump(status, f)
    with open(os.path.join(a.out, "trainer_status.json"), "w") as f:
        json.dump(status, f)
if __name__ == "__main__":
    main()
    sys.exit(0)
