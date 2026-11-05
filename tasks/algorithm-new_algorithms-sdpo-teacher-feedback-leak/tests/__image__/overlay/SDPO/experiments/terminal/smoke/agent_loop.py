"""Tool agent loop for terminal tasks: every trajectory gets its own workspace (the task's public files, if any), which
the bash tool works in and which is handed to the reward (non_tensor_batch["workspace"]) when the trajectory ends."""

import os
import shutil
import uuid
from pathlib import Path
from typing import Any

from verl.experimental.agent_loop.agent_loop import AgentLoopOutput
from verl.experimental.agent_loop.tool_agent_loop import AgentState, ToolAgentLoop

NOBODY = 65534


def new_workspace(task_id: str) -> Path:
    root = Path(os.environ["SMOKE_RUN_DIR"]) / "workspaces"
    root.mkdir(parents=True, exist_ok=True)
    ws = root / uuid.uuid4().hex
    public = Path(os.environ.get("TERMINAL_POOL", "/data/sdpo_terminal/pool")) / "tasks" / task_id / "public"
    if public.is_dir():
        shutil.copytree(public, ws)
    else:
        ws.mkdir()
    if os.geteuid() == 0:
        for dp, dn, fn in os.walk(ws):
            for p in [dp] + [os.path.join(dp, f) for f in fn]:
                os.chown(p, NOBODY, NOBODY)
    return ws


class TerminalToolAgentLoop(ToolAgentLoop):
    async def run(self, sampling_params: dict[str, Any], **kwargs) -> AgentLoopOutput:
        extra_info = kwargs.get("extra_info") or {}
        self._workspace = await self.loop.run_in_executor(None, new_workspace, extra_info["task_id"])
        output = await super().run(sampling_params, **kwargs)
        output.extra_fields["workspace"] = str(self._workspace)
        return output

    async def _handle_pending_state(self, agent_data, sampling_params: dict[str, Any]) -> AgentState:
        agent_data.extra_fields["workspace"] = str(self._workspace)
        return await super()._handle_pending_state(agent_data, sampling_params)
