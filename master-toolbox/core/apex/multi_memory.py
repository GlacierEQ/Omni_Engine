import os
import asyncio
import json
from typing import Dict, Any
from mem0 import MemoryClient, AsyncMemoryClient

MEM0_KEYS = {
    "PRIMARY_PRO": "m0-bjuFyuiIvBcaj7c1KXSlUkogNPifL5GT2vU5zrjj",
    "SECONDARY_CASEY": "m0-XsPsE19WZoEesvOFYbm9A6Du98pWS8wyfHUXJ60U"
}

class MultiMemoryOrchestrator:
    def __init__(self):
        self.mem0_primary = MemoryClient(api_key=MEM0_KEYS["PRIMARY_PRO"])
        self.mem0_secondary = MemoryClient(api_key=MEM0_KEYS["SECONDARY_CASEY"])
        print("🧬 [APEX] Dual Mem0 Cluster: ONLINE")

    async def sink(self, payload: Dict[str, Any]):
        """Sinks data into the multi-memory backup layer"""
        content = str(payload.get("agent_data", []))
        user_id = f"{payload.get('case_id', 'default')}_backup"
        return self.mem0_secondary.add(messages=[{"role": "user", "content": content}], user_id=user_id)

    async def powerhouse_sync(self, content: str, user_id: str, case_id: str):
        self.mem0_primary.add(messages=[{"role": "user", "content": content}], user_id=user_id)
        self.mem0_secondary.add(messages=[{"role": "user", "content": content}], user_id=f"{user_id}_backup")
        return {"status": "FULLY_SYNCED", "layers": 5, "case": case_id}

    def get_integrated_context(self, query: str, user_id: str):
        primary_ctx = self.mem0_primary.search(query=query, filters={"AND": [{"user_id": user_id}]})
        return primary_ctx
