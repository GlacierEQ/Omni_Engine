from typing import Dict, Any, List
import time

class NotionMcpRouter:
    """
    Routes Notion calls to a canonical MCP server with fallbacks.
    """
    def __init__(self, mcp_client, servers: List[str] = None):
        self.mcp = mcp_client
        self.servers = servers or ["notion", "smithery-notion", "mingxiao300-notion-smithery"]

    async def health_check(self) -> Dict[str, Any]:
        """
        Basic health = can list tools for at least one Notion server.
        """
        for s in self.servers:
            res = await self.mcp.list_tools(s)
            if res.get("ok"):
                return {"ok": True, "server": s, "checked": self.servers}
        return {"ok": False, "error": "No Notion MCP server reachable", "checked": self.servers}

    async def call(self, tool: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Try canonical then fallbacks.
        """
        last = None
        for s in self.servers:
            res = await self.mcp.call(s, tool, params)
            if res.get("ok"):
                res["server"] = s
                return res
            last = res
        return {"ok": False, "error": "All Notion MCP servers failed", "last": last, "servers": self.servers}
