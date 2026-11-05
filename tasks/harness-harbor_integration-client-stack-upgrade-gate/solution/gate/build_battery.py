import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
EPISODES = Path(os.environ.get("GATE_EPISODES", "/app/episodes"))
LAUNCH = Path(os.environ.get("GATE_LAUNCH", "/app/launch"))
MODELS = Path(os.environ.get("GATE_MODELS", "/models"))
MI_EVAL = {"max_input_tokens": 65536, "max_output_tokens": 8192, "input_cost_per_token": 0, "output_cost_per_token": 0}
def eval_config(ckpt: Path) -> tuple[dict, str]:
    p = ckpt / "eval_config.json"
    c = json.loads(p.read_text()) if p.exists() else {}
    kw = {"model_info": MI_EVAL, "temperature": float(c.get("temperature", 0.6)), "parser_name": c.get("parser_name", "json"),
          "interleaved_thinking": str(c.get("interleaved_thinking", "false")).lower() == "true"}
    samp = {k: c[k] for k in ("top_p", "top_k") if c.get(k) is not None}
    if samp:
        kw["llm_call_kwargs"] = {"extra_body": samp}
    tok = Path(json.loads((ckpt / "checkpoint.json").read_text())["tokenizer_dir"])
    tok = MODELS / tok.name
    base = (tok / "chat_template.jinja").read_text()
    think = c.get("enable_thinking")
    think = ("false" if "enable_thinking is true" in base else "true") if think is None else str(think).lower()
    if c.get("chat_template") == "miles_fixed":
        tpl = "{%- set preserve_thinking = true %}\n" + "{%- set enable_thinking = " + think + " %}\n" + \
              (LAUNCH / "templates" / "qwen3.5_fixed.jinja").read_text()
    else:
        tpl = "{%- set enable_thinking = " + think + " %}\n" + base
    return kw, tpl
def rollout_configs() -> dict[str, tuple[dict, str]]:
    env = {}
    for line in (LAUNCH / "rollout" / "recipe.env").read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k] = v.strip("'\"")
    req = {"temperature": float(env["ROLLOUT_TEMPERATURE"]), "top_p": float(env["ROLLOUT_TOP_P"]),
           "top_k": int(env["ROLLOUT_TOP_K"]), "max_tokens": int(env["ROLLOUT_MAX_RESPONSE_LEN"]),
           "skip_special_tokens": env["ROLLOUT_SKIP_SPECIAL_TOKENS"].lower() == "true", "no_stop_trim": True,
           "spaces_between_special_tokens": False}
    sys.path.insert(0, str(LAUNCH / "rollout"))
    old = dict(os.environ)
    out = {}
    try:
        os.environ.update({k: v for k, v in env.items() if k.startswith(("AGENT_", "HARBOR_"))})
        import terminus_agent as ta
        tpl = "{%- set preserve_thinking = true %}\n{%- set enable_thinking = true %}\n" + \
              (LAUNCH / "templates" / "qwen3.5_fixed.jinja").read_text()
        os.environ["HARBOR_COLLECT_ROLLOUT_DETAILS"] = "0"
        kw = ta.terminus_kwargs("http://x", "sk-session-local", req, {"session_id": "rollout-0001"})
        kw.pop("api_base")
        out["rl_rollout"] = (kw, tpl)
        os.environ["HARBOR_COLLECT_ROLLOUT_DETAILS"] = "1"
        kw = ta.terminus_kwargs("http://x", "sk-session-local", req, {"session_id": "rollout-0001"})
        kw.pop("api_base")
        out["rl_tokens"] = (kw, tpl)
    finally:
        os.environ.clear()
        os.environ.update(old)
    return out
def conv(trial: Path, dst: Path, cfg: str, max_steps: int = 0):
    cmd = [sys.executable, "-I", str(HERE / "rig" / "from_trial.py"), str(trial), str(dst), cfg]
    if max_steps:
        cmd += ["--max-steps", str(max_steps)]
    subprocess.run(cmd, check=True, capture_output=True)
def inflate(ep: Path, target_chars: int = 8500, repeat: int = 3):
    e = json.loads((ep / "task" / "environment" / "episode.json").read_text())
    eng = json.loads((ep / "engine.json").read_text())
    chunks = []
    for r in range(repeat):
        for i, c in enumerate(e["chunks"]):
            lines, n = [], 0
            k = 0
            while n < target_chars:
                s = f"[{r}:{i:03d}:{k:04d}] make[2]: Building C object src/CMakeFiles/core.dir/mod_{(i * 31 + k) % 997:03d}.c.o -- 0x{(r * 7919 + i * 104729 + k * 1299709) % 4294967291:08x}"
                lines.append(s)
                n += len(s) + 1
                k += 1
            body = c.rstrip("\n").split("\n")
            prompt = body[-1] if body else ""
            chunks.append("\n".join(body[:-1] + lines + [prompt]) + "\n")
    e["chunks"] = chunks
    eng["responses"] = [r for _ in range(repeat) for r in eng["responses"] if "task_complete" not in r["content"] and
                        "<task_complete>true" not in r["content"]] + [r for r in eng["responses"] if "task_complete" in r["content"] or "<task_complete>true" in r["content"]]
    (ep / "task" / "environment" / "episode.json").write_text(json.dumps(e, ensure_ascii=False))
    (ep / "engine.json").write_text(json.dumps(eng, ensure_ascii=False))
def main():
    out = Path(sys.argv[1])
    if out.exists():
        shutil.rmtree(out)
    (out / "episodes").mkdir(parents=True)
    (out / "templates").mkdir()
    configs, served = {}, {}
    for ckpt in sorted((LAUNCH / "checkpoints").iterdir()):
        kw, tpl = eval_config(ckpt)
        name = f"eval_{ckpt.name}"
        configs[name] = {"model": "hosted_vllm/policy", "kwargs": kw}
        (out / "templates" / f"{name}.jinja").write_text(tpl)
        served[name] = f"{name}.jinja"
    for name, (kw, tpl) in rollout_configs().items():
        configs[name] = {"model": "hosted_vllm/policy", "kwargs": kw}
        (out / "templates" / f"{name}.jinja").write_text(tpl)
        served[name] = f"{name}.jinja"
    (out / "configs.json").write_text(json.dumps(configs, indent=1))
    (out / "served.json").write_text(json.dumps(served, indent=1))
    json_cfgs = [c for c in configs if configs[c]["kwargs"].get("parser_name") == "json"]
    xml_cfgs = [c for c in configs if configs[c]["kwargs"].get("parser_name") == "xml"]
    base = []
    for ck in sorted(EPISODES.iterdir()):
        for trial in sorted(ck.iterdir()):
            own = f"eval_{ck.name}"
            name = f"{own}__{trial.name.lower().replace('_', '-')}"
            conv(trial, out / "episodes" / name, own)
            base.append((name, trial, own))
            parser = json.loads((trial / "config.json").read_text())["agent"]["kwargs"].get("parser_name", "json")
            for other in (json_cfgs if parser == "json" else xml_cfgs):
                if other != own:
                    conv(trial, out / "episodes" / f"{other}__{trial.name.lower().replace('_', '-')}", other)
            lname = f"long_{own}__{trial.name.lower().replace('_', '-')}"
            conv(trial, out / "episodes" / lname, own)
            inflate(out / "episodes" / lname)
            if parser == "xml":
                lname = f"long_rl_rollout__{trial.name.lower().replace('_', '-')}"
                conv(trial, out / "episodes" / lname, "rl_rollout")
                inflate(out / "episodes" / lname)
    js = [b for b in base if configs[b[2]]["kwargs"]["parser_name"] == "json"]
    xs = [b for b in base if configs[b[2]]["kwargs"]["parser_name"] == "xml"]
    spec = []
    def add(name, b, **kw):
        spec.append(dict(base=b, name=name, **kw))
    fault_bases = [js[0][0], xs[0][0], xs[1][0]]
    for j, b in enumerate(fault_bases):
        t = f"f{j}"
        for nm, fl in {"http500": {"2": "http500"}, "http502": {"3": "http502"},
                       "http503x3": {"2": "http503", "3": "http503", "4": "http503"}, "reset": {"2": "reset"},
                       "http429": {"2": "http429"}, "badjson": {"2": "badjson"}, "empty": {"2": "empty_choices"},
                       "http500x4": {"2": "http500", "3": "http500", "4": "http500", "5": "http500"},
                       "ctx400": {"4": "ctx400"}, "ctx400x2": {"4": "ctx400", "5": "ctx400"}}.items():
            add(f"fault_{t}__{nm}", b, faults=fl)
        for kind in ("http500", "reset", "ctx400", "badjson"):
            add(f"persist_{t}__{kind}", b, persist={"from": 3, "kind": kind},
                kwargs_override={"max_turns": 8, "suppress_max_turns_warning": True})
    add("hang_h0__agent_timeout", js[1][0], faults={"3": {"kind": "hang", "secs": 45}}, agent_timeout=15)
    rewards = {"nan": {"reward.txt": "nan\n"}, "inf": {"reward.txt": "inf\n"}, "neg": {"reward.txt": "-1\n"},
               "space": {"reward.txt": " 1 \n"}, "float": {"reward.txt": "1.0\n"}, "sci": {"reward.txt": "1e0\n"},
               "half": {"reward.txt": "0.5\n"}, "empty": {"reward.txt": ""}, "none": {},
               "jint": {"reward.json": "{\"reward\": 1}"}, "jstr": {"reward.json": "{\"reward\": \"1\"}"},
               "jmulti": {"reward.json": "{\"reward\": 1, \"tests_passed\": 3}"}, "jnull": {"reward.json": "{\"reward\": null}"},
               "jbool": {"reward.json": "{\"reward\": true}"}, "jnan": {"reward.json": "{\"reward\": NaN}"},
               "jlist": {"reward.json": "[1]"}, "jbad": {"reward.json": "{\"reward\": 1"},
               "both": {"reward.txt": "0\n", "reward.json": "{\"reward\": 1}"}}
    for j, b in enumerate([js[2][0], xs[2][0]]):
        t = f"r{j}"
        for rn, files in rewards.items():
            add(f"reward_{t}__{rn}", b, reward_files=files)
        add(f"reward_{t}__rc1", b, verifier_rc=1, reward_files={"reward.txt": "0\n"})
        add(f"stale_{t}__txt_none", b, reward_files={}, effects={"1": {"/logs/verifier/reward.txt": "1\n"}})
        add(f"stale_{t}__json_over_txt", b, reward_files={"reward.txt": "0\n"}, effects={"1": {"/logs/verifier/reward.json": "{\"reward\": 1}"}})
        add(f"stale_{t}__txt_kept", b, reward_files={"reward.txt": "0\n"}, effects={"1": {"/logs/verifier/reward.txt": "1\n"}})
    add("resp_e0__think_in_content", js[3][0], response_edits=[{"i": i, "op": "think_in_content"} for i in range(6)])
    add("resp_e1__empty_content", js[3][0], response_edits=[{"i": i, "op": "empty_content"} for i in (1, 2)])
    add("resp_e2__length", js[4][0], response_edits=[{"i": 2, "op": "length"}])
    add("resp_e3__length", xs[3][0], response_edits=[{"i": 2, "op": "length"}])
    for j, b in enumerate([js[5][0], xs[4][0]]):
        add(f"setup_s{j}__tmux_missing", b, tmux_missing=True)
        add(f"setup_s{j}__install_timeout", b, tmux_missing=True, install_timeout=True)
        add(f"setup_s{j}__install_runtime_error", b, tmux_missing=True, install_runtime_error=True)
    (out / "variants.json").write_text(json.dumps(spec, indent=0))
    subprocess.run([sys.executable, "-I", str(HERE / "rig" / "make_variants.py"), str(out), str(out / "variants.json")],
                   check=True, capture_output=True)
    print("battery:", len(list((out / "episodes").iterdir())), "trials,", len(configs), "launch configs")
if __name__ == "__main__":
    main()
