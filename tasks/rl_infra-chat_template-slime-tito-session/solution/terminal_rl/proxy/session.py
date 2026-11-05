import hashlib
import asyncio
import copy
import json
import logging
import time
from slime.utils.types import Sample
logger = logging.getLogger(__name__)
def render_request(tokenizer, body: dict, default_kwargs: dict | None = None) -> str:
    messages = copy.deepcopy(body["messages"])
    for i, m in enumerate(messages):
        if m.get("content") is None:
            m["content"] = ""
        if not isinstance(m.get("content"), list):
            m = messages[i] = {k: v for k, v in m.items() if v is not None}
        if m.get("role") == "assistant" and isinstance(m.get("tool_calls"), list):
            for item in m["tool_calls"]:
                fn = item.get("function") or {}
                if isinstance(fn.get("arguments"), str):
                    fn["arguments"] = json.loads(fn["arguments"])
    kwargs = dict(default_kwargs or {})
    kwargs.update(body.get("chat_template_kwargs") or {})
    reasoning_effort = body.get("reasoning_effort", "medium")
    if kwargs.get("reasoning_effort") is not None:
        reasoning_effort = kwargs["reasoning_effort"]
    kwargs.pop("reasoning_effort", None)
    tools = body.get("tools")
    try:
        return tokenizer.apply_chat_template(messages, tools=tools, tokenize=False, add_generation_prompt=True,
                                             reasoning_effort=reasoning_effort, **kwargs)
    except Exception:
        if not tools:
            raise
        flat = [t["function"] if "function" in t else t for t in tools]
        return tokenizer.apply_chat_template(messages, tools=flat, tokenize=False, add_generation_prompt=True,
                                             reasoning_effort=reasoning_effort, **kwargs)
def _decoder_types(tokenizer) -> list[dict]:
    backend = getattr(tokenizer, "backend_tokenizer", None)
    if backend is None:
        return []
    out, todo = [], [json.loads(backend.to_str()).get("decoder")]
    while todo:
        d = todo.pop()
        if d and d.get("type") == "Sequence":
            todo.extend(d.get("decoders") or [])
        elif d:
            out.append(d)
    return out
def _sentencepiece_bytes(piece: str) -> bytes:
    if len(piece) == 6 and piece.startswith("<0x") and piece.endswith(">"):
        try:
            return bytes([int(piece[3:5], 16)])
        except ValueError:
            pass
    return piece.replace("▁", " ").encode("utf-8")
class TokenText:
    def __init__(self, tokenizer):
        from transformers.models.gpt2.tokenization_gpt2 import bytes_to_unicode
        u2b = {v: k for k, v in bytes_to_unicode().items()}
        self._bytes: dict[int, bytes] = {}
        model = getattr(tokenizer, "model", None)
        decoders = _decoder_types(tokenizer)
        sentencepiece = not any(d.get("type") == "ByteLevel" for d in decoders) and any(
            d.get("type") in ("ByteFallback", "Metaspace")
            or (d.get("type") == "Replace" and (d.get("pattern") or {}).get("String") == "▁") for d in decoders)
        if model is not None and hasattr(model, "decode_single_token_bytes"):
            for i in range(model.n_vocab):
                try:
                    self._bytes[i] = model.decode_single_token_bytes(i)
                except KeyError:
                    pass
        elif sentencepiece:
            for s, i in tokenizer.get_vocab().items():
                self._bytes[i] = _sentencepiece_bytes(s)
        else:
            for s, i in tokenizer.get_vocab().items():
                try:
                    self._bytes[i] = bytes(u2b[c] for c in s)
                except KeyError:
                    self._bytes[i] = s.encode("utf-8")
        special = set(getattr(tokenizer, "all_special_ids", None) or [])
        for i, t in tokenizer.added_tokens_decoder.items():
            if sentencepiece and not (t.special or int(i) in special):
                self._bytes[int(i)] = _sentencepiece_bytes(t.content)
            else:
                self._bytes[int(i)] = t.content.encode("utf-8")
    def __call__(self, ids) -> bytes:
        return b"".join(self._bytes[int(i)] for i in ids)
class Snapshot:
    __slots__ = ("parent", "tail", "tail_bytes", "length", "nbytes", "generation")
    def __init__(self, parent, tail: list[int], tail_bytes: bytes, generation=None):
        self.parent = parent
        self.tail = tail
        self.tail_bytes = tail_bytes
        self.length = (parent.length if parent else 0) + len(tail)
        self.nbytes = (parent.nbytes if parent else 0) + len(tail_bytes)
        self.generation = generation
    def ids(self) -> list[int]:
        parts, node = [], self
        while node is not None:
            parts.append(node.tail)
            node = node.parent
        out = []
        for p in reversed(parts):
            out.extend(p)
        return out
class Generation:
    __slots__ = ("prompt", "output_ids", "log_probs", "finish_reason", "parent", "sample", "end")
    def __init__(self, prompt: Snapshot, output_ids, log_probs, finish_reason, parent):
        self.prompt = prompt
        self.output_ids = output_ids
        self.log_probs = log_probs
        self.finish_reason = finish_reason
        self.parent = parent
        self.sample = None
        self.end: Snapshot | None = None
class Session:
    def __init__(self, sid: str, tokenizer, token_text: TokenText, default_kwargs: dict | None = None):
        self.sid = sid
        self.tokenizer = tokenizer
        self.token_text = token_text
        self.default_kwargs = dict(default_kwargs or {})
        self.lock = asyncio.Lock()
        self.snapshots: list[Snapshot] = []
        self.generations: list[Generation] = []
        self._by_key: dict[tuple, Generation] = {}
        self._by_target: dict[bytes, list[Generation]] = {}
        self.created = time.time()
    def _is_prefix(self, snap: Snapshot, target: bytes, memo: dict) -> bool:
        key = id(snap)
        if key in memo:
            return memo[key]
        ok = snap.nbytes <= len(target)
        if ok and snap.parent is not None:
            ok = self._is_prefix(snap.parent, target, memo)
        if ok:
            start = snap.nbytes - len(snap.tail_bytes)
            ok = target[start : snap.nbytes] == snap.tail_bytes
        memo[key] = ok
        return ok
    def prompt_for(self, body: dict) -> tuple[Snapshot, Snapshot | None]:
        text = render_request(self.tokenizer, body, self.default_kwargs)
        fresh = self.tokenizer.encode(text, add_special_tokens=False)
        target = self.token_text(fresh)
        tkey = hashlib.sha1(target).digest()
        for g in self._by_target.pop(tkey, []):
            self.rollback(g)
        self._last_tkey = tkey
        memo: dict = {}
        best = None
        for snap in self.snapshots:
            if snap.nbytes < len(target) and (target[snap.nbytes] & 0xC0) == 0x80:
                continue
            if (best is None or snap.nbytes > best.nbytes) and self._is_prefix(snap, target, memo):
                best = snap
        tail = None
        if best is not None:
            rest = target[best.nbytes :].decode("utf-8")
            tail = self.tokenizer.encode(rest, add_special_tokens=False) if rest else []
            if self.token_text(tail) != target[best.nbytes :]:
                best, tail = None, None
        if tail is None:
            tail, best = fresh, None
        prompt = Snapshot(best, list(tail), self.token_text(tail))
        if prompt.nbytes != len(target):
            raise RuntimeError(f"session {self.sid}: prompt ids do not reproduce the rendered prompt")
        return prompt, best
    def rollback(self, gen: "Generation"):
        if gen in self.generations:
            self.generations.remove(gen)
        if gen.end in self.snapshots:
            self.snapshots.remove(gen.end)
        self._by_key = {k: g for k, g in self._by_key.items() if g is not gen}
    def add_generation(self, prompt: Snapshot, base: Snapshot | None, output_ids, log_probs, finish_reason):
        prompt_ids = prompt.ids()
        key = (tuple(prompt_ids), tuple(output_ids))
        if key in self._by_key:
            return self._by_key[key]
        parent, node = None, base
        while node is not None and parent is None:
            if node.generation is not None and node.generation in self.generations:
                parent = node.generation
            node = node.parent
        gen = Generation(prompt, list(output_ids), list(log_probs), finish_reason, parent)
        gen.end = Snapshot(prompt, list(output_ids), self.token_text(output_ids), generation=gen)
        if prompt.tail or prompt.parent is None:
            self.snapshots.append(prompt)
        self.snapshots.append(gen.end)
        self.generations.append(gen)
        self._by_key[key] = gen
        self._by_target.setdefault(self._last_tkey, []).append(gen)
        return gen
    def to_samples(self) -> list[Sample]:
        samples: list[dict] = []
        for gen in self.generations:
            prompt_ids = gen.prompt.ids()
            parent = gen.parent
            if parent is not None and parent.sample is not None and parent.sample["tip"] is parent:
                s = parent.sample
                bridge = prompt_ids[len(s["tokens"]) :]
                s["tokens"].extend(bridge)
                s["mask"].extend([0] * len(bridge))
                s["lp"].extend([0.0] * len(bridge))
            else:
                s = {"tokens": list(prompt_ids), "prompt_len": len(prompt_ids), "mask": [], "lp": [], "turns": 0,
                     "truncated": False}
                samples.append(s)
            s["tokens"].extend(gen.output_ids)
            s["mask"].extend([1] * len(gen.output_ids))
            s["lp"].extend(gen.log_probs)
            s["turns"] += 1
            s["truncated"] = gen.finish_reason == "length"
            s["tip"] = gen
            gen.sample = s
        out = []
        for k, s in enumerate(samples):
            out.append(
                Sample(
                    tokens=s["tokens"],
                    response_length=len(s["tokens"]) - s["prompt_len"],
                    loss_mask=s["mask"],
                    rollout_log_probs=s["lp"],
                    status=Sample.Status.TRUNCATED if s["truncated"] else Sample.Status.COMPLETED,
                    session_id=self.sid,
                    metadata={"num_turns": s["turns"], "branch": k, "num_branches": len(samples),
                              "conversation": self.sid},
                )
            )
        return out
class SessionStore:
    def __init__(self, tokenizer, default_kwargs: dict | None = None):
        self.tokenizer = tokenizer
        self.token_text = TokenText(tokenizer)
        self.default_kwargs = dict(default_kwargs or {})
        self._episodes: dict[str, dict[str, Session]] = {}
    def get(self, sid: str, conversation: str | None = None) -> Session:
        convs = self._episodes.setdefault(sid, {})
        cid = conversation or sid
        session = convs.get(cid)
        if session is None:
            session = convs[cid] = Session(cid, self.tokenizer, self.token_text, self.default_kwargs)
        return session
    def finish(self, sid: str) -> list[Sample]:
        convs = self._episodes.pop(sid, None)
        if convs is None:
            logger.warning("finish for unknown session %s", sid)
            return []
        out = []
        for session in sorted(convs.values(), key=lambda c: c.created):
            out.extend(session.to_samples())
        return out
    def __len__(self):
        return len(self._episodes)
