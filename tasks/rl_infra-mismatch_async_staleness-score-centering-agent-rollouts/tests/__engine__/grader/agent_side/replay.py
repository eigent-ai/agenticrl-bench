import json
import os
import httpx
_DATA = None
CURRENT = {"uid": None, "tool_i": 0, "rewards": {}}
def data():
    global _DATA
    if _DATA is None:
        with open(os.environ["SC_REPLAY_FILE"]) as f:
            _DATA = json.load(f)
    return _DATA
tool_specs = None
def _load_specs():
    global tool_specs
    tool_specs = data()["__tools__"]
_load_specs()
async def agent(base_url: str, prompt, request_kwargs: dict | None = None, metadata: dict | None = None, **kwargs):
    uid = (metadata or {})["replay_uid"]
    rec = data()[uid]
    recorded = rec["messages"]
    messages = [m for m in recorded[:1]]
    i = 1
    t = 0
    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
        while i < len(recorded) and recorded[i]["role"] == "assistant":
            payload = {"model": "default", "messages": messages, "tools": tool_specs, **(request_kwargs or {})}
            if t == 0 and rec.get("first_turn_top_p") is not None:
                payload["top_p"] = rec["first_turn_top_p"]
            r = await client.post(base_url + "/v1/chat/completions", json=payload)
            if r.status_code != 200:
                raise RuntimeError(f"replay turn {t} of {uid}: HTTP {r.status_code}: {r.text[:500]}")
            message = r.json()["choices"][0]["message"]
            tool_calls = message.get("tool_calls") or []
            assistant = {"role": "assistant", "content": message.get("content")}
            if message.get("reasoning_content"):
                assistant["reasoning_content"] = message["reasoning_content"]
            if tool_calls:
                assistant["tool_calls"] = tool_calls
            messages.append(assistant)
            i += 1
            k = 0
            while i < len(recorded) and recorded[i]["role"] == "tool":
                tool = dict(recorded[i])
                if k < len(tool_calls):
                    tool["tool_call_id"] = tool_calls[k].get("id")
                messages.append(tool)
                i += 1
                k += 1
            t += 1
    return {"replay_uid": uid}
async def execute_tool(name: str, params: dict) -> str:
    rec = data()[CURRENT["uid"]]
    flat = [c for turn in rec["tool_outputs"] for c in turn]
    i = CURRENT["tool_i"]
    CURRENT["tool_i"] = i + 1
    if i >= len(flat):
        return "Error: replay has no further tool output"
    return flat[i]
async def reward(args, sample, **kwargs):
    if isinstance(sample, list):
        return [await reward(args, s, **kwargs) for s in sample]
    uid = (sample.metadata or {}).get("replay_uid") or CURRENT["uid"]
    return float(CURRENT["rewards"][uid])
