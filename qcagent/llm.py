"""Thin model clients with one shared interface.

Messages are kept in a neutral format and converted per provider:
  {"role": "user", "content": str}
  {"role": "assistant", "content": str, "tool_calls": [{"id", "name", "args"}]}
  {"role": "tool", "tool_call_id": str, "name": str, "content": str}

client.chat(system, messages, tools) -> Reply(text, tool_calls, in_tokens, out_tokens)
`tools` may be None/[] to forbid tool use.
"""
from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, field


@dataclass
class Reply:
    text: str
    tool_calls: list = field(default_factory=list)  # [{"id","name","args"}]
    in_tokens: int = 0
    out_tokens: int = 0


class AnthropicClient:
    def __init__(self, model: str | None = None, max_tokens: int = 2048):
        import anthropic
        self.client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
        self.model = model or os.environ.get("QC_ANTHROPIC_MODEL", "claude-sonnet-5-5")
        self.max_tokens = max_tokens

    def _convert(self, messages):
        out = []
        for m in messages:
            if m["role"] == "user":
                out.append({"role": "user", "content": m["content"]})
            elif m["role"] == "assistant":
                blocks = []
                if m.get("content"):
                    blocks.append({"type": "text", "text": m["content"]})
                for tc in m.get("tool_calls", []):
                    blocks.append({"type": "tool_use", "id": tc["id"], "name": tc["name"],
                                   "input": tc["args"]})
                out.append({"role": "assistant", "content": blocks or " "})
            elif m["role"] == "tool":
                block = {"type": "tool_result", "tool_use_id": m["tool_call_id"],
                         "content": m["content"]}
                # consecutive tool results go in one user turn
                if out and out[-1]["role"] == "user" and isinstance(out[-1]["content"], list):
                    out[-1]["content"].append(block)
                else:
                    out.append({"role": "user", "content": [block]})
        return out

    def chat(self, system, messages, tools=None) -> Reply:
        kw = dict(model=self.model, max_tokens=self.max_tokens, system=system,
                  messages=self._convert(messages), temperature=0)
        if tools:
            kw["tools"] = [{"name": t["name"], "description": t["description"],
                            "input_schema": t["parameters"]} for t in tools]
        r = self.client.messages.create(**kw)
        text = "".join(b.text for b in r.content if b.type == "text")
        calls = [{"id": b.id, "name": b.name, "args": dict(b.input or {})}
                 for b in r.content if b.type == "tool_use"]
        return Reply(text, calls, r.usage.input_tokens, r.usage.output_tokens)


class OllamaClient:
    """Local open-weight model through Ollama's /api/chat (tool-calling capable models)."""

    def __init__(self, model: str | None = None, host: str | None = None):
        self.model = model or os.environ.get("QC_OLLAMA_MODEL", "qwen2.5:7b-instruct")
        self.host = (host or os.environ.get("OLLAMA_HOST", "http://localhost:11434")).rstrip("/")

    def _convert(self, system, messages):
        out = [{"role": "system", "content": system}]
        for m in messages:
            if m["role"] == "assistant":
                out.append({"role": "assistant", "content": m.get("content", ""),
                            "tool_calls": [{"function": {"name": tc["name"],
                                                         "arguments": tc["args"]}}
                                           for tc in m.get("tool_calls", [])]})
            elif m["role"] == "tool":
                out.append({"role": "tool", "content": m["content"], "tool_name": m["name"]})
            else:
                out.append({"role": "user", "content": m["content"]})
        return out

    def chat(self, system, messages, tools=None) -> Reply:
        import requests
        body = {"model": self.model, "messages": self._convert(system, messages),
                "stream": False, "options": {"temperature": 0, "num_ctx": 16384}}
        if tools:
            body["tools"] = [{"type": "function", "function": t} for t in tools]
        r = requests.post(f"{self.host}/api/chat", json=body, timeout=600)
        r.raise_for_status()
        d = r.json()
        msg = d.get("message", {})
        calls = []
        for tc in msg.get("tool_calls") or []:
            f = tc.get("function", {})
            args = f.get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {}
            calls.append({"id": uuid.uuid4().hex[:12], "name": f.get("name", ""), "args": args})
        return Reply(msg.get("content", "") or "", calls,
                     d.get("prompt_eval_count", 0), d.get("eval_count", 0))


class ScriptedClient:
    """Replays a fixed list of Reply objects. For tests only."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.model = "scripted"

    def chat(self, system, messages, tools=None) -> Reply:
        if not self.replies:
            return Reply('{"bugs": []}')
        return self.replies.pop(0)


def make_client(name: str):
    if name == "claude":
        return AnthropicClient()
    if name == "qwen":
        return OllamaClient()
    raise ValueError(f"unknown model {name!r} (use 'claude', 'qwen', or 'rules')")
