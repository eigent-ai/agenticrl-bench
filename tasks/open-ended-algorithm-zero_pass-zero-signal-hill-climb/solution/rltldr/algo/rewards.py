"""RLTL;DR rewards -> advantages (reward_post_process).

Objective (paper): L = L_GRPO + lambda * L_SFT, each the mean over its own samples of the per-token-mean loss.
Miles averages per ROLLOUT (an episode and its insight-SFT siblings share one rollout_id): rollout r contributes
sum_{tokens of r} adv * l / M_r, M_r = loss-mask tokens of r, and the step divides by the number of rollouts (= N_rl).
Matching both terms exactly:
  episode i (length L_i):    adv = A_i * M_r / L_i        (= A_i when the rollout has no SFT sibling)
  SFT sample j (length L_j): adv = lambda * M_r * N_rl / (L_j * N_sft)
A_i = GRPO normalisation by group_index (insight-conditioned episodes have their own group ids). Episodes stopped by
the box's training wall cap are left out of the statistics and get advantage 0 (oneclick_hooks); an SFT sibling of a
capped episode is kept (its insight came from an earlier, uncapped failure).
"""
from collections import defaultdict

from examples.terminal_agent.oneclick_hooks import _flat, grpo_normalize_excluding, is_wall_capped

from algo.config import CFG


def _mask_len(s) -> int:
    if is_wall_capped(s):
        return 0
    return int(sum(s.loss_mask)) if s.loss_mask is not None else int(s.response_length or 0)


def post_process(args, samples):
    samples = _flat(samples)
    lam = float(CFG.get("insight_sft", 0.0))
    raw = [float(s.get_reward_value(args)) for s in samples]
    is_sft = [(s.metadata or {}).get("algo_kind") == "sft_insight" for s in samples]
    rl_idx = [i for i, f in enumerate(is_sft) if not f]
    rl = [samples[i] for i in rl_idx]
    rl_adv = grpo_normalize_excluding(args, rl, [raw[i] for i in rl_idx], [is_wall_capped(x) for x in rl])
    base = dict(zip(rl_idx, rl_adv))
    n_rl, n_sft = len(rl_idx), sum(is_sft)
    m_r = defaultdict(int)

    def key(s, i):
        return s.rollout_id if s.rollout_id is not None else ("row", i)

    for i, s in enumerate(samples):
        m_r[key(s, i)] += _mask_len(s)
    adv = []
    for i, s in enumerate(samples):
        L, M = max(1, _mask_len(s)), m_r[key(s, i)]
        if is_sft[i]:
            adv.append(lam * M * n_rl / (L * max(1, n_sft)))
        elif is_wall_capped(s):
            adv.append(0.0)
        else:
            adv.append(base[i] * M / L)
    return raw, adv
