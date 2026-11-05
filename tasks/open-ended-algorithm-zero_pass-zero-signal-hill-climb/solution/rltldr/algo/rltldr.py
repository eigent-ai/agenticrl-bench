"""RLTL;DR (arXiv 2609.37633) as a generate plug-in: K-attempt chains with self-written insights, lambda * insight SFT.

Per task and step, the group of n slots is split into U plain slots (the task as deployed, no notes) and C = n - U
chains. Chain j advances one attempt per step: attempt 1 has no notes; after a failed attempt the policy itself, in a
fresh context (rlsdk.policy: the task text, that attempt's own last commands and outputs, the environment's sanitized
checker report from rlsdk.feedback, the chain's earlier insights), writes a one-sentence insight; attempt k is the task
plus the insights 1..k-1. A pass, or K attempts, restarts the chain. A chain with no history starts from one of the
base model's screening reports (/data/eval), so step 0 already runs attempt 2.
GRPO baselines per (task, context kind): plain-context samples form one group, insight-conditioned samples another.
With lambda > 0, each new insight also yields an SFT sample (insight-writer prompt with the task text only -> the
policy's own insight), returned next to the episode; algo.rewards gives it the exact lambda weight.
Every trained token is a token the policy generated, trained in the context it was sampled in (episodes), or the
policy's own insight text (SFT).
"""
from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path

from rlsdk import policy
from rlsdk.feedback import feedback_text, parse_verifier_dir
from rlsdk.paths import task_dir

from algo import state
from algo.config import CFG
from algo.tail import tail_from_trajectory

COND_GROUP_OFFSET = 10**9
SFT_GROUP_OFFSET = 2 * 10**9
_BASE = None
_TOK = None

INSIGHT_SYSTEM = "You review a failed attempt at a terminal task and write one short lesson for the next attempt."
INSIGHT_USER = """Task:
{task}
{earlier}
The last commands of the failed attempt and their outputs (most recent last):
{tail}

The checker's report on that attempt:
{report}

Write ONE sentence (at most 30 words): the single most useful, concrete lesson for the next attempt at this task.
Reply with the sentence only."""
SFT_USER = """Task:
{task}

Write ONE sentence (at most 30 words): the single most useful, concrete lesson for an attempt at this task.
Reply with the sentence only."""


def _base():
    global _BASE
    if _BASE is None:
        from miles.rollout.generate_hub.agentic_tool_call import generate as default_generate

        _BASE = default_generate
    return _BASE


def _tokenizer(args):
    global _TOK
    if _TOK is None:
        from transformers import AutoTokenizer

        _TOK = AutoTokenizer.from_pretrained(os.environ.get("MSWEA_TOKENIZER_PATH") or args.hf_checkpoint)
    return _TOK


def _chains_path(task_id: str) -> Path:
    return state.ROOT / "chains" / f"{state.safe(task_id)}.json"


def _load_chains(task_id: str, c: int) -> list[dict]:
    p = _chains_path(task_id)
    ch = json.loads(p.read_text()) if p.exists() else []
    while len(ch) < c:
        ch.append({"insights": [], "attempt": 1, "n_chain": 0, "seeded": False})
    return ch


def _save_chains(task_id: str, ch: list[dict]) -> None:
    p = _chains_path(task_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(ch))
    tmp.replace(p)


async def _write_insight(args, task_text: str, tail: str, report: str, earlier: list[str]) -> str | None:
    ear = ("\nYour notes from earlier failed attempts:\n" + "\n".join(f"- {x}" for x in earlier) + "\n") if earlier else ""
    msgs = [{"role": "system", "content": INSIGHT_SYSTEM},
            {"role": "user", "content": INSIGHT_USER.format(task=task_text[:6000], tail=tail, report=report, earlier=ear)}]
    text = await policy.chat(args, msgs, max_tokens=int(CFG.get("insight_max_tokens", 512)),
                             temperature=float(CFG.get("insight_temperature", 0.7)), enable_thinking=False)
    if not text:
        return None
    text = text.split("</think>", 1)[1] if "</think>" in text else text
    line = next((x.strip() for x in text.strip().splitlines() if x.strip()), "")
    return line[:300] or None


def _notes(insights: list[str]) -> str:
    lines = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(insights))
    return ("Notes you wrote after earlier failed attempts at this task (most recent last); the environment has been "
            f"reset since then:\n{lines}")


def _sft_sample(args, src, task_text: str, insight: str):
    """(insight-writer prompt with the task text only -> the policy's own insight), loss on the insight tokens."""
    from miles.utils.types import Sample

    tok = _tokenizer(args)
    msgs = [{"role": "system", "content": INSIGHT_SYSTEM}, {"role": "user", "content": SFT_USER.format(task=task_text[:6000])}]
    prompt_ids = tok.encode(tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True,
                                                    enable_thinking=False), add_special_tokens=False)
    end = tok.convert_tokens_to_ids("<|im_end|>")
    resp = tok.encode(insight, add_special_tokens=False) + ([end] if isinstance(end, int) and end >= 0 else [])
    s = deepcopy(src)
    s.tokens = list(prompt_ids) + resp
    s.response_length = len(resp)
    s.loss_mask = [1] * len(resp)
    s.rollout_log_probs = [0.0] * len(resp)
    s.response = insight
    s.reward = 0.0
    s.status = Sample.Status.COMPLETED
    s.metadata = {"algo_kind": "sft_insight", "algo_mode": "sft", "reward": 0.0,
                  "instance_id": (src.metadata or {}).get("instance_id")}
    s.group_index = SFT_GROUP_OFFSET + int(src.index or 0)
    s.rollout_id = src.rollout_id if src.rollout_id is not None else int(src.index or 0)
    for attr in ("teacher_log_probs", "rollout_topk_token_ids", "rollout_topk_log_probs", "rollout_routed_experts"):
        if hasattr(s, attr):
            setattr(s, attr, None)
    return s


async def generate(input):
    from miles.rollout.base_types import GenerateFnOutput

    args, sample = input.args, input.sample
    md = dict(sample.metadata or {})
    task_id = str(md.get("instance_id"))
    g = int(args.n_samples_per_prompt)
    u = min(g, int(CFG.get("plain_slots", 2)))
    k_max = int(CFG.get("max_attempts", 8))
    slot = int(sample.index or 0) % g
    step = int(sample.group_index or 0) // max(1, int(args.rollout_batch_size))
    tdir = task_dir(task_id)
    task_text = (tdir / "instruction.md").read_text() if (tdir / "instruction.md").exists() else ""
    chain_j = slot - u if (not input.evaluation and slot >= u) else None
    insights, attempt, seed_insight = [], 1, None
    if chain_j is not None:
        state.ensure_seeded()
        seed = None
        with state.locked(_chains_path(task_id)):
            ch = _load_chains(task_id, g - u)
            if not ch[chain_j]["insights"] and not ch[chain_j]["seeded"]:
                seed = state.pick_feedback(task_id, key=f"{task_id}|seed|{chain_j}")
                ch[chain_j]["seeded"] = True
            _save_chains(task_id, ch)
        if seed is not None:
            seed_insight = await _write_insight(args, task_text, seed.get("tail") or "(not available)", seed["text"], [])
            with state.locked(_chains_path(task_id)):
                ch = _load_chains(task_id, g - u)
                if seed_insight:
                    ch[chain_j]["insights"].append(seed_insight)
                    ch[chain_j]["attempt"] = 2
                _save_chains(task_id, ch)
        with state.locked(_chains_path(task_id)):
            c = _load_chains(task_id, g - u)[chain_j]
        insights, attempt = list(c["insights"]), int(c["attempt"])
    mode = "cond" if insights else "plain"
    if insights:
        md["algo_notes"] = _notes(insights)
    sample.metadata = md

    out = await _base()(input)

    produced = out.samples if isinstance(out.samples, list) else [out.samples]
    for s in produced:
        s.metadata = {**(s.metadata or {}), "algo_mode": mode, "algo_attempt": attempt}
        s.metadata.pop("algo_notes", None)
        if mode == "cond" and s.group_index is not None:
            s.group_index = int(s.group_index) + COND_GROUP_OFFSET
    head = produced[0].metadata if produced else {}
    reward = float(head.get("reward", 0.0) or 0.0)
    trial_dir = head.get("trial_dir")
    parsed = parse_verifier_dir(Path(trial_dir) / "verifier") if trial_dir else {"ok": False}
    report = feedback_text(parsed, tdir) if (trial_dir and parsed.get("ok")) else None
    if report and reward < 1:
        state.add_feedback(task_id, report, int(parsed.get("n_passed") or 0), step, mode)
    new_insight = None
    if chain_j is not None:
        if reward >= 1 or attempt >= k_max:
            with state.locked(_chains_path(task_id)):
                ch = _load_chains(task_id, g - u)
                ch[chain_j] = {"insights": [], "attempt": 1, "n_chain": ch[chain_j]["n_chain"] + 1, "seeded": True}
                _save_chains(task_id, ch)
        elif report:
            tail = tail_from_trajectory(Path(trial_dir) / "agent" / "mini_trajectory.json")
            new_insight = await _write_insight(args, task_text, tail, report, insights)
            with state.locked(_chains_path(task_id)):
                ch = _load_chains(task_id, g - u)
                if new_insight:
                    ch[chain_j]["insights"].append(new_insight)
                ch[chain_j]["attempt"] = attempt + 1
                _save_chains(task_id, ch)
    lam = float(CFG.get("insight_sft", 0.0))
    sft = [_sft_sample(args, sample, task_text, x) for x in (seed_insight, new_insight) if x] if lam > 0 else []
    if sft:  # siblings of one generate() share one rollout_id (Miles' compact-rollout check)
        rid = produced[0].rollout_id if produced[0].rollout_id is not None else int(produced[0].index or 0)
        for x in produced + sft:
            x.rollout_id = rid
    state.log_episode({"task_id": task_id, "step": step, "slot": slot, "chain": chain_j, "attempt": attempt,
                       "mode": mode, "reward": reward, "n_passed": parsed.get("n_passed"), "n_tests": parsed.get("n_tests"),
                       "insights_in_context": insights, "seed_insight": seed_insight, "new_insight": new_insight,
                       "n_sft": len(sft), "lambda": lam, "trial_dir": trial_dir})
    return GenerateFnOutput(samples=list(produced) + sft)
