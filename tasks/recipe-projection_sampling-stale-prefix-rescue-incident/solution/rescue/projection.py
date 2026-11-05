from __future__ import annotations
import json
import math
import random
from dataclasses import dataclass
from miles.utils.misc import load_function
from miles.utils.types import Sample
from .episode import Episode, EpisodeRunner
@dataclass
class ChainResult:
    episode: Episode
    init_tries: int
    proposals: int
    accepted: int
    passed: int
def _suffix_sum(values: list[float], ep: Episode, j: int) -> float:
    start = ep.turns[j][0]
    return sum(v for v, m in zip(values[start:], ep.mask()[start:], strict=True) if m)
class ProjectionSampler:
    def __init__(self, args, runner: EpisodeRunner):
        self.args = args
        self.runner = runner
        self.steps = args.rescue_mcmc_steps
        self.init_attempts = args.rescue_init_attempts
        self.reward_fn = load_function(args.custom_rm_path)
        self.rng = random.Random(args.rollout_seed)
    async def passes(self, template: Sample, ep: Episode) -> bool:
        if not ep.finished:
            return False
        probe = Sample(prompt=template.prompt, label=template.label, response=ep.text, metadata=dict(template.metadata))
        reward = await self.reward_fn(self.args, probe)
        return bool(reward["acc"]) if isinstance(reward, dict) else reward > 0
    async def score_student(self, prompt_ids: list[int], ep: Episode) -> None:
        ep.student = await self.runner.token_logprobs(prompt_ids + ep.ids, len(prompt_ids))
    async def run(self, template: Sample, prompt_ids: list[int], hinted_ids: list[int]) -> ChainResult | None:
        cur = None
        tries = 0
        for tries in range(1, self.init_attempts + 1):
            ep = await self.runner.continue_episode(hinted_ids, Episode())
            if await self.passes(template, ep):
                cur = ep
                break
        if cur is None:
            return None
        await self.score_student(prompt_ids, cur)
        proposals = accepted = passed = 0
        for _ in range(self.steps):
            j = self.rng.randrange(cur.num_turns)
            cand = await self.runner.continue_episode(hinted_ids, cur.prefix(j))
            proposals += 1
            if not await self.passes(template, cand):
                continue
            passed += 1
            await self.score_student(prompt_ids, cand)
            log_r = (
                _suffix_sum(cand.student, cand, j) - _suffix_sum(cur.student, cur, j)
                + _suffix_sum(cur.logprobs, cur, j) - _suffix_sum(cand.logprobs, cand, j)
                + math.log(cur.num_turns) - math.log(cand.num_turns)
            )
            if log_r >= 0 or self.rng.random() < math.exp(log_r):
                cur = cand
                accepted += 1
        return ChainResult(cur, tries, proposals, accepted, passed)
def gold_query(sample: Sample) -> str:
    return json.loads(sample.label)["query"]
