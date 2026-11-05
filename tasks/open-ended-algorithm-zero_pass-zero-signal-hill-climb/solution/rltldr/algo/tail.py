"""A failed attempt's own last commands and their outputs (for the insight writer)."""
import json
import re

ACTION = re.compile(r"```mswea_bash_command\s*\n(.*?)\n```", re.DOTALL)


def tail_from_messages(msgs, n: int = 6) -> str:
    pairs = []
    for i, m in enumerate(msgs or []):
        if m.get("role") != "assistant":
            continue
        reply = m.get("content") or ""
        reply = reply.split("</think>", 1)[1] if "</think>" in reply else reply
        acts = ACTION.findall(reply)
        obs = msgs[i + 1]["content"] if i + 1 < len(msgs) and msgs[i + 1].get("role") == "user" else ""
        if acts:
            pairs.append((acts[0].strip()[:300], re.sub(r"\s+", " ", obs or "")[:400]))
    if not pairs:
        return "(no commands)"
    return "\n".join(f"$ {c}\n{o}" for c, o in pairs[-n:])


def tail_from_trajectory(path) -> str:
    try:
        return tail_from_messages(json.loads(open(path).read()).get("messages") or [])
    except (OSError, ValueError):
        return "(not available)"
