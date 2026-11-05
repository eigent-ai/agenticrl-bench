"""Replay one recorded dump through the OPD reward hooks of a code snapshot, the way the rollout calls them (and the way
/app/tools/replay_opd.py does): reward_func per sample (concurrently, result stored in sample.reward), then
post_process_rewards(args, samples). Writes what the hooks produced as JSON. Started by /opt/live/run.sh as an
unprivileged user.

usage: live_case.py <case.json> <episodes.jsonl> <out.json>
"""
import argparse
import asyncio
import importlib
import json
import math
import os
import sys
import time
import traceback

MILES = os.environ["MILES_DIR"]


def build_args(case):
    a = argparse.Namespace(
        hf_checkpoint=case["student_dir"],
        rm_url=case["rm_url"],
        apply_chat_template_kwargs=case["student_kwargs"],
        tito_model="qwen35",
        use_session_server=True,
        rollout_temperature=1.0,
        rollout_max_response_len=2048,
        max_seq_len=16384,
        rollout_batch_size=16,
        n_samples_per_prompt=4,
        custom_rm_path="examples.terminal_opd.reward.reward_func",
        custom_reward_post_process_path="examples.terminal_opd.reward.post_process_rewards",
        custom_config_path=case["teacher_yaml_path"],
        use_opd=True,
        opd_type="sglang",
        opd_kl_coef=1.0,
        opd_log_prob_top_k=0,
        opd_top_k_strategy="only-student",
        opd_reward_weight_mode="student_p",
        opd_topk_per_position=False,
        opd_teacher_urls=None,
        opd_teacher_key="opd_teacher",
        sglang_router_request_timeout_secs=None,
        advantage_estimator="grpo",
        rewards_normalization=True,
        grpo_std_normalization=True,
    )
    for k, v in case["teacher_yaml"].items():
        setattr(a, k, v)
    return a


def main():
    case = json.load(open(sys.argv[1]))
    rows = [json.loads(line) for line in open(sys.argv[2])]
    out = {"kind": case["kind"], "ok": False}
    t0 = time.time()
    try:
        sys.path.insert(0, MILES)
        from miles.utils.types import Sample

        samples = [Sample.from_dict(r) for r in rows]
        args = build_args(case)
        mod = importlib.import_module("examples.terminal_opd.reward")
        reward_func, post_process = mod.reward_func, mod.post_process_rewards

        async def score_all():
            sem = asyncio.Semaphore(16)

            async def one(s):
                async with sem:
                    s.reward = await reward_func(args, s)

            await asyncio.gather(*(one(s) for s in samples))

        asyncio.run(score_all())
        raw, rewards = post_process(args, samples)
        res = []
        for s in samples:
            t = s.teacher_log_probs
            if t is None:
                vals = None
            else:
                try:
                    vals = [float(v) for v in (t.tolist() if hasattr(t, "tolist") else list(t))]
                except Exception:  # noqa: BLE001
                    vals = None
            if vals is not None:
                vals = [v if math.isfinite(v) else repr(v) for v in vals]
            res.append({
                "index": s.index,
                "teacher_log_probs": vals,
                "tokens": list(s.tokens),
                "loss_mask": list(s.loss_mask) if s.loss_mask is not None else None,
                "rollout_log_probs": [float(v) for v in s.rollout_log_probs] if s.rollout_log_probs else [],
                "response_length": s.response_length,
            })
        out.update(ok=True, samples=res, raw_rewards=[float(r) for r in raw], rewards=[float(r) for r in rewards])
    except BaseException as e:  # noqa: BLE001 - the hooks may raise anything
        out["error"] = f"{type(e).__name__}: {e}"[:2000]
        out["trace"] = traceback.format_exc()[-4000:]
    out["seconds"] = time.time() - t0
    with open(sys.argv[3], "w") as f:
        json.dump(out, f)


if __name__ == "__main__":
    main()
