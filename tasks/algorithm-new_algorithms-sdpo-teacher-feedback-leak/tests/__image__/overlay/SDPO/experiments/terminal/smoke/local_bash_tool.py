"""`bash` tool for the smoke run: runs the command in the trajectory's own workspace on this box (the sandbox fleet's
stand-in). The workspace comes from the agent loop (agent_data.extra_fields["workspace"]); commands run unprivileged
(uid/gid 65534) when the trainer runs as root, with a wall-clock limit and an output cap."""

import asyncio
import os
import signal
from typing import Any

from verl.tools.base_tool import BaseTool
from verl.tools.schemas import ToolResponse

NOBODY = 65534
SAFE_PATH = "/usr/local/go/bin:/usr/local/cargo/bin:/usr/local/bin:/usr/bin:/bin"


class LocalBashTool(BaseTool):
    def __init__(self, config: dict, tool_schema):
        super().__init__(config, tool_schema)
        self.timeout = float(config.get("timeout", 30))
        self.max_output = int(config.get("max_output_bytes", 65536))

    async def execute(self, instance_id: str, parameters: dict[str, Any], **kwargs) -> tuple[ToolResponse, float, dict]:
        agent_data = kwargs.get("agent_data")
        workspace = getattr(agent_data, "extra_fields", {}).get("workspace") if agent_data is not None else None
        command = parameters.get("command") if isinstance(parameters, dict) else None
        if not workspace or not os.path.isdir(workspace):
            return ToolResponse(text="error: no workspace for this trajectory"), 0.0, {}
        if not isinstance(command, str) or not command.strip():
            return ToolResponse(text="error: missing 'command'"), 0.0, {}
        prefix = []
        if os.geteuid() == 0:
            prefix = ["/usr/bin/setpriv", f"--reuid={NOBODY}", f"--regid={NOBODY}", "--clear-groups", "--"]
        env = {"PATH": SAFE_PATH, "HOME": workspace, "LANG": "C.UTF-8", "TERM": "dumb", "PYTHONDONTWRITEBYTECODE": "1",
               "RUSTUP_HOME": "/usr/local/rustup", "CARGO_HOME": os.path.join(workspace, ".cargo"),
               "GOTOOLCHAIN": "local", "GOFLAGS": "-mod=mod", "TMPDIR": "/tmp"}
        proc = await asyncio.create_subprocess_exec(
            *prefix, "/bin/bash", "-c", command, cwd=workspace, env=env, stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT, start_new_session=True)
        chunks, size, timed_out = [], 0, False

        async def pump():
            nonlocal size
            while True:
                b = await proc.stdout.read(8192)
                if not b:
                    return
                if size < self.max_output:
                    chunks.append(b[: self.max_output - size])
                size += len(b)
                if size >= self.max_output:
                    _kill(proc.pid)

        try:
            await asyncio.wait_for(pump(), timeout=self.timeout)
        except asyncio.TimeoutError:
            timed_out = True
            _kill(proc.pid)
        try:
            rc = await asyncio.wait_for(proc.wait(), timeout=10)
        except asyncio.TimeoutError:
            rc = -9
        text = b"".join(chunks).decode("utf-8", "replace")
        if timed_out:
            text += f"\n[command timed out after {self.timeout:.0f}s]"
        elif size > self.max_output:
            text += "\n[output truncated]"
        if rc not in (0, None) and not timed_out:
            text += f"\n[exit code {rc}]"
        return ToolResponse(text=text), 0.0, {}


def _kill(pid: int):
    try:
        os.killpg(pid, signal.SIGKILL)
    except OSError:
        pass
