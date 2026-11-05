import argparse
import json
import re
from pathlib import Path
TOML = """schema_version = "1.1"
[task]
name = "replay/{name}"
[agent]
timeout_sec = {agent_timeout}
[verifier]
timeout_sec = 600.0
[environment]
build_timeout_sec = 60.0
cpus = 1
memory_mb = 2048
"""
def split_message(msg: str):
    analysis, plan = "", ""
    m = re.match(r"(?s)^Analysis: (.*?)(?:\nPlan: (.*))?$", msg or "")
    if m:
        analysis, plan = m.group(1) or "", m.group(2) or ""
    elif (msg or "").startswith("Plan: "):
        plan = msg[6:]
    else:
        analysis = msg or ""
    return analysis, plan
def render(parser, analysis, plan, cmds, complete):
    if parser == "xml":
        ks = "".join(f'<keystrokes duration="{c["duration"]}">{c["keystrokes"]}</keystrokes>\n' for c in cmds)
        tc = "<task_complete>true</task_complete>\n" if complete else ""
        return (f"<response>\n<analysis>\n{analysis}\n</analysis>\n<plan>\n{plan}\n</plan>\n"
                f"<commands>\n{ks}</commands>\n{tc}</response>")
    obj = {"analysis": analysis, "plan": plan, "commands": cmds}
    if complete:
        obj["task_complete"] = True
    return json.dumps(obj, indent=2, ensure_ascii=False)
def obs_text(step):
    res = ((step.get("observation") or {}).get("results") or [])
    txt = "".join(r.get("content") or "" for r in res if isinstance(r, dict))
    for marker in ("New Terminal Output:\n\n", "New Terminal Output:\n", "Current Terminal Screen:\n"):
        i = txt.find(marker)
        if i >= 0:
            body = txt[i + len(marker):]
            j = body.find("\n\nAre you sure you want to mark the task as complete?")
            return body[:j] if j >= 0 else body, marker.startswith("New")
    return None, False
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("trial")
    ap.add_argument("out")
    ap.add_argument("config")
    ap.add_argument("--max-steps", type=int, default=0)
    ap.add_argument("--reward", default=None, help="override reward.txt content")
    a = ap.parse_args()
    trial, out = Path(a.trial), Path(a.out)
    cfg = json.loads((trial / "config.json").read_text())
    kw = cfg["agent"]["kwargs"]
    parser = kw.get("parser_name", "json")
    traj = json.loads((trial / "agent" / "trajectory.json").read_text())
    steps = traj["steps"]
    first = steps[0]["message"]
    m = re.search(r"(?s)Task Description:\n(.*?)\n\n+Current terminal state:\n(?:Current Terminal Screen:\n)?(.*)$", first)
    instruction, screen = (m.group(1), m.group(2)) if m else ("(instruction)", "root@modal:/app# \n")
    responses, chunks = [], []
    n = 0
    for s in steps[1:]:
        if s.get("source") != "agent" or s.get("is_copied_context"):
            continue
        n += 1
        if a.max_steps and n > a.max_steps:
            break
        calls = s.get("tool_calls") or []
        cmds = [{"keystrokes": c["arguments"].get("keystrokes", ""), "duration": c["arguments"].get("duration", 1.0)}
                for c in calls if c.get("function_name") == "bash_command"]
        complete = any(c.get("function_name") == "mark_task_complete" for c in calls)
        analysis, plan = split_message(s.get("message") or "")
        if not calls and not analysis and not plan:
            content = (s.get("message") or "").strip() or "I need to look at the terminal again."
        else:
            content = render(parser, analysis, plan, cmds, complete)
        responses.append({"content": content, "reasoning_content": s.get("reasoning_content")})
        if cmds:
            t, new = obs_text(s)
            chunks.append(t if (t is not None and new) else "")
    res = json.loads((trial / "result.json").read_text())
    rew = ((res.get("verifier_result") or {}).get("rewards") or {}).get("reward")
    reward = a.reward if a.reward is not None else ("" if rew is None else f"{int(rew) if float(rew).is_integer() else rew}\n")
    name = out.name
    (out / "task" / "environment").mkdir(parents=True, exist_ok=True)
    (out / "task" / "tests").mkdir(parents=True, exist_ok=True)
    (out / "task" / "task.toml").write_text(TOML.format(name=name, agent_timeout=900.0))
    (out / "task" / "instruction.md").write_text(instruction.rstrip("\n") + "\n")
    (out / "task" / "environment" / "Dockerfile").write_text("FROM debian:bookworm-slim\nWORKDIR /app\n")
    (out / "task" / "tests" / "test.sh").write_text("#!/bin/bash\nbash /tests/run_checks.sh\n")
    ep = {"initial_screen": screen, "chunks": chunks,
          "verifier": {"files": ({"reward.txt": reward} if reward else {}), "rc": 0, "stdout": "checks done\n"}}
    (out / "task" / "environment" / "episode.json").write_text(json.dumps(ep, ensure_ascii=False))
    tail = {"content": render(parser, "The work is finished.", "Mark the task complete.", [], True), "reasoning_content": None}
    (out / "engine.json").write_text(json.dumps({"responses": responses, "faults": {}, "tail": tail}, ensure_ascii=False))
    (out / "launch.json").write_text(json.dumps({"config": a.config, "source": str(trial)}))
    print(name, parser, len(responses), "turns", len(chunks), "chunks", "reward", repr(reward))
if __name__ == "__main__":
    main()
