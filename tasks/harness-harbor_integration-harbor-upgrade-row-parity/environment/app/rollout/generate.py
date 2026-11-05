"""Our generate / reward hooks for terminal RL on Miles (``--custom-generate-function-path generate.generate``,
``--custom-rm-path generate.reward_func``).

``generate`` is Miles' ``agentic_tool_call.generate`` (session server + the agent function in
``harbor_agent_function.py``) plus one rule of ours: an episode the agent function reports as an infrastructure
failure (``exit_status == "InfraError"``) comes back ABORTED, so ``check_no_aborted`` keeps it out of the batch
instead of training it as a reward-0 negative.

``reward_func`` reads the reward the agent function put in the sample metadata (same as the swe-agent example).
"""

from miles.rollout.base_types import GenerateFnInput, GenerateFnOutput
from miles.rollout.generate_hub import agentic_tool_call
from miles.utils.types import Sample

INFRA_EXIT_STATUSES = frozenset({"InfraError"})


async def generate(input: GenerateFnInput) -> GenerateFnOutput:
    output = await agentic_tool_call.generate(input)
    samples = output.samples if isinstance(output.samples, list) else [output.samples]
    for sample in samples:
        if (sample.metadata or {}).get("exit_status") in INFRA_EXIT_STATUSES:
            sample.status = Sample.Status.ABORTED
    return output


generate.add_arguments = agentic_tool_call.generate.add_arguments


async def reward_func(args, samples: Sample | list[Sample], **kwargs) -> float | list[float]:
    if isinstance(samples, list):
        return [s.metadata.get("reward", 0.0) for s in samples]
    return samples.metadata.get("reward", 0.0)
