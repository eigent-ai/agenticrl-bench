import json
from functools import lru_cache
from pathlib import Path
import jinja2
from jinja2.sandbox import ImmutableSandboxedEnvironment
SAMPLING_DEFAULTS = {
    "temperature": 1.0, "top_p": 1.0, "top_k": -1, "min_p": 0.0, "repetition_penalty": 1.0,
    "presence_penalty": 0.0, "frequency_penalty": 0.0, "max_tokens": None, "stop": None, "stop_token_ids": None,
    "n": 1, "seed": None, "logprobs": False, "top_logprobs": None, "return_token_ids": False,
    "skip_special_tokens": True, "ignore_eos": False, "response_format": None, "chat_template_kwargs": None,
    "tools": None, "tool_choice": None, "min_tokens": 0, "logit_bias": None,
    "no_stop_trim": False, "spaces_between_special_tokens": True, "separate_reasoning": True, "stream_reasoning": True,
}
ALIASES = {"max_completion_tokens": "max_tokens"}
def _tojson(x, ensure_ascii=False, indent=None, separators=None, sort_keys=False):
    return json.dumps(x, ensure_ascii=ensure_ascii, indent=indent, separators=separators, sort_keys=sort_keys)
def _raise(msg):
    raise jinja2.exceptions.TemplateError(msg)
@lru_cache(maxsize=None)
def compiled(path):
    env = ImmutableSandboxedEnvironment(trim_blocks=True, lstrip_blocks=True, extensions=["jinja2.ext.loopcontrols"])
    env.filters["tojson"] = _tojson
    env.globals["raise_exception"] = _raise
    return env.from_string(Path(path).read_text())
def sglang_message(m):
    d = {"role": m.get("role"), "content": m.get("content"), "reasoning_content": m.get("reasoning_content"),
         "tool_calls": m.get("tool_calls"), "name": m.get("name"), "tool_call_id": m.get("tool_call_id")}
    c = d["content"]
    if isinstance(c, list):
        d["content"] = "".join(p.get("text", "") for p in c if isinstance(p, dict) and p.get("type") == "text")
    return d
def render(body, template):
    msgs = [sglang_message(m) for m in body.get("messages") or []]
    kw = dict(body.get("chat_template_kwargs") or {})
    return compiled(template).render(messages=msgs, tools=body.get("tools"), add_generation_prompt=True, **kw)
def sampling(body):
    eb = body.get("extra_body") if isinstance(body.get("extra_body"), dict) else {}
    out = {}
    for k, dflt in SAMPLING_DEFAULTS.items():
        v = body.get(k, eb.get(k))
        for a, t in ALIASES.items():
            if t == k and v is None:
                v = body.get(a, eb.get(a))
        if k == "logprobs" and v is None:
            v = False
        out[k] = dflt if v is None else v
    for k in ("temperature", "top_p", "min_p", "repetition_penalty", "presence_penalty", "frequency_penalty"):
        try:
            out[k] = float(out[k])
        except (TypeError, ValueError):
            pass
    return out
def view(body, template):
    return {"prompt": render(body, template), "sampling": sampling(body)}
