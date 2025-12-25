import os
import asyncio
from typing import List, Dict, Any
from mem0 import MemoryClient, AsyncMemoryClient
from core.apex.multi_memory import MultiMemoryOrchestrator

MEM0_KEYS = {
    "PRIMARY": "m0-bjuFyuiIvBcaj7c1KXSlUkogNPifL5GT2vU5zrjj",
    "SECONDARY": "m0-XsPsE19WZoEesvOFYbm9A6Du98pWS8wyfHUXJ60U"
}

class ApexMem0Master:
    def __init__(self, key_type: str = "PRIMARY"):
        self.api_key = MEM0_KEYS.get(key_type, MEM0_KEYS["PRIMARY"])
        os.environ["MEM0_API_KEY"] = self.api_key
        self.client = MemoryClient(api_key=self.api_key)
        self.async_client = AsyncMemoryClient(api_key=self.api_key)
        self.orchestrator = MultiMemoryOrchestrator()
        print(f"🚀 Apex Mem0 Master Initialized | Multi-Memory Orchestrator ACTIVE")

    async def ingest(self, payload: Dict[str, Any]):
        """Real ingestion logic for A2S synthesis"""
        content = str(payload.get("agent_data", []))
        user_id = payload.get("case_id", "default_user")
        return self.client.add(messages=[{"role": "user", "content": content}], user_id=user_id)

    def system_audit(self):
        return {"status": "ACTIVE", "protocol": "APEX-v2", "orchestrator": "ONLINE"}

    def semantic_retrieval(self, query: str, user_id: str):
        filters = {"AND": [{"user_id": user_id}]}
        return self.client.search(query=query, filters=filters)

    async def parallel_ingest(self, items: List[str], user_id: str):
        tasks = [
            self.async_client.add(messages=[{"role": "user", "content": item}], user_id=user_id)
            for item in items
        ]
        return await asyncio.gather(*tasks, return_exceptions=True)

    def store(self, content: str, user_id: str, metadata: Dict = None):
        asyncio.create_task(self.orchestrator.powerhouse_sync(content, user_id, "1FDV-23-0001009"))
        return self.client.add(
            messages=[{"role": "user", "content": content}],
            user_id=user_id,
            metadata=metadata or {}
        )

    def fetch_user_history(self, user_id: str):
        return self.client.get_all(filters={"AND": [{"user_id": user_id}]})
