# Score centering — reading notes

Paper: Martin Marek & Max Ryabinin, *Score Centering Stabilizes Off-policy Reinforcement Learning*,
arXiv:2609.20807 (Sep 2026). These are our notes from the reading group; equation numbers follow the paper.

## Why

Policy gradient computes `E[R * grad log p(y)]`, but the rollout tokens come from the sampler `q`
(our fp8 SGLang engine, possibly a few weights behind), while the score `grad log p` is computed by the
trainer `p` (bf16 Megatron). At a fixed prefix, write `s_v = grad log p_v` for every vocabulary token `v`
and `s_bar = sum_v q_v s_v` (expected score under the sampler). Then

    E_q[R s_y] = E_q[R] * s_bar  +  Cov_q(R, s_y)          (eq. 3)
                 \___ drift ___/    \___ signal ___/

On-policy `s_bar = 0`; under mismatch it is not, and the drift term distills the trainer toward the
sampler at every prefix with a non-zero expected advantage. Group centering does not remove it.

## Method

Replace the score of the sampled token by the centered score (eq. 4):

    s~_y = s_y - s_bar,       E_q[s~_y] = 0 at every prefix, even off-policy.

It is a no-op on-policy (`p = q`), it adds no importance ratio, and it composes with importance sampling.

### Top-k approximation (App. A.1)

Storing the sampler's full next-token distribution is too expensive, so the sampler logs its top-k
log-probs (k = 128 in the paper; k = 32 is reported to work as well). With head `H` (the stored
candidates) and tail `T` (everything else), the sampler distribution is reconstructed as

    q^_v = q_v          for v in H
    q^_v = rho * p_v    for v in T,     rho = (1 - sum_{v in H} q_v) / (1 - sum_{v in H} p_v)     (eq. 7)

and because `E_p[s] = 0`,

    E_q^[s] = sum_{v in H} (q_v - rho p_v) s_v                                                   (eq. 8)

so only the k head tokens are needed. Both tail masses are floored at `eps = 1e-6`.

### Composition with importance sampling (App. A.2)

With weights `w_v = f(p_v / q_v)`, center the weighted score:

    R * (w_y s_y - E_q[w s]),      E_q^[w^ s] = sum_{v in H} (q_v w_v - alpha p_v) s_v,
    alpha = rho * f(1 / rho)                                                                     (eq. 9-10)

- vanilla score centering: `f(r) = 1`, `alpha = rho`
- TIS: `f(r) = min(r, c)`, c = 2 in the paper
- MIS: `f(r) = r` if `low <= r <= high` else 0, with low = 0.5, high = 5
- sanity check: plain IS `f(r) = r` gives `alpha = 1` and `q_v w_v = p_v`, i.e. nothing left to center.

### As a loss (App. A.3)

Per generated token, with stop-gradient `sg` on every weight and coefficient:

    L = -A * ( sg[w_y] * log p_y  -  sum_{v in H} sg[q_v w_v - alpha p_v] * log p_v )            (eq. 12)

`-grad L = A * (w_y s_y - E_q^[w s])`. The sampled token always uses the sampler's recorded log-prob for
its weight, also when it is not among the k stored candidates. The sampler probabilities must be the ones
recorded when the token was generated; rescoring old rollouts with newer weights would replace the
behaviour policy.

### Training objective used in the paper (App. B.1)

REINFORCE with group-centered rewards, `A_i = R_i - mean(R_group)`, no std normalisation, token-level
mean over the batch, one optimizer step per batch. No PPO clipping.

## Paper results we care about

- fp8 W/A sampler vs bf16 trainer (Qwen3-30B-A3B): SC matches or beats TIS/MIS/PPO-style corrections, and
  the gap grows with the mismatch.
- Staleness: SC + TIS beats TIS alone.
- k = 128 head covers > 99.9% of sampler mass on average in their settings; overhead < 1% wall-clock.
