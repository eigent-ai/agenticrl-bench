"""SQL data agent as an OpenAI-style client of the Miles session server.

    --custom-generate-function-path miles.rollout.generate_hub.agentic_tool_call.generate
    --custom-agent-function-path examples.sql_agent.agent.run_agent
    --use-session-server v2 --tito-model qwen35

Per-row options from the dataset's metadata column:
    first_turn_top_p   top_p for the first (schema exploration) call; later calls use the session defaults.
The transcript (tool outputs included) is returned as metadata so the reward function can read the answer.
"""

import json
from copy import deepcopy

import httpx

from examples.sql_agent.sql_tool import TOOL_CONFIGS, execute_tool, tool_specs


async def run_agent(base_url: str, prompt, request_kwargs: dict | None = None, metadata: dict | None = None, **kwargs):
    messages = deepcopy(prompt) if isinstance(prompt, list) else [{"role": "user", "content": prompt}]
    request_kwargs = dict(request_kwargs or {})
    first_turn_top_p = (metadata or {}).get("first_turn_top_p")
    tool_calls_made = 0
    async with httpx.AsyncClient(timeout=httpx.Timeout(600.0)) as client:
        for turn in range(TOOL_CONFIGS["max_turns"]):
            payload = {"model": "default", "messages": messages, "tools": tool_specs, **request_kwargs}
            if turn == 0 and first_turn_top_p is not None:
                payload["top_p"] = first_turn_top_p
            response = await client.post(base_url + "/v1/chat/completions", json=payload)
            response.raise_for_status()
            choice = response.json()["choices"][0]
            message = choice["message"]
            tool_calls = message.get("tool_calls") or []
            assistant = {"role": "assistant", "content": message.get("content")}
            if message.get("reasoning_content"):
                assistant["reasoning_content"] = message["reasoning_content"]
            if tool_calls:
                assistant["tool_calls"] = tool_calls
            messages.append(assistant)
            if not tool_calls or choice.get("finish_reason") == "length":
                break
            for call in tool_calls:
                name = call["function"]["name"]
                raw = call["function"].get("arguments") or "{}"
                try:
                    params = json.loads(raw) if isinstance(raw, str) else raw
                except json.JSONDecodeError:
                    params = {}
                output = await execute_tool(name, params if isinstance(params, dict) else {})
                tool_calls_made += 1
                messages.append({"role": "tool", "tool_call_id": call.get("id"), "content": output, "name": name})
    return {"messages": messages, "tool_call_count": tool_calls_made}
