import asyncio
import json
import os
from typing import Dict, Any, Optional

class McpCliClient:
    """
    MCP client adapter using local `mcp` CLI.
    Works in Smithery-like environments where mcp is present.
    """
    def __init__(self, timeout_s: int = 60):
        self.timeout_s = timeout_s

    async def _run(self, *args: str) -> Dict[str, Any]:
        # Run `mcp ...` and capture stdout
        proc = await asyncio.create_subprocess_exec(
            "mcp", *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        try:
            out, err = await asyncio.wait_for(proc.communicate(), timeout=self.timeout_s)
        except asyncio.TimeoutError:
            proc.kill()
            return {"ok": False, "error": "timeout", "args": ["mcp", *args]}

        out_s = out.decode(errors="replace").strip()
        err_s = err.decode(errors="replace").strip()

        # Try JSON parse first; if not JSON, return raw
        try:
            data = json.loads(out_s) if out_s else None
            return {"ok": proc.returncode == 0, "data": data, "stdout": out_s, "stderr": err_s}
        except Exception:
            return {"ok": proc.returncode == 0, "data": None, "stdout": out_s, "stderr": err_s}

    async def list_tools(self, server: str) -> Dict[str, Any]:
        # Many MCP CLIs support `mcp <server>` to show tools.
        return await self._run(server)

    async def call(self, server: str, tool: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assumption: CLI supports:
          mcp <server> <tool> '<json>'
        """
        payload = json.dumps(params, separators=(",", ":"), ensure_ascii=False)
        return await self._run(server, tool, payload)
