from typing import List, Dict, Any
import os
import asyncio
import json
from mem0 import MemoryClient, AsyncMemoryClient

# 🔑 APEX CREDENTIALS
MEM0_KEYS = {
    "PRIMARY": "m0-bjuFyuiIvBcaj7c1KXSlUkogNPifL5GT2vU5zrjj", # higuy.vids@gmail.com
    "SECONDARY": "m0-XsPsE19WZoEesvOFYbm9A6Du98pWS8wyfHUXJ60U" # casey@hi-classhomeservices.com
}

class ApexMem0Master:
    """
    Unified Apex-Tier Mem0 Orchestrator.
    Hierarchy: Architecture (T1) -> Logic (T2) -> Concurrency (T3) -> Integration (T4) -> Core (T5).
    """

    def __init__(self, key_type: str = "PRIMARY"):
        self.api_key = MEM0_KEYS.get(key_type, MEM0_KEYS["PRIMARY"])
        os.environ["MEM0_API_KEY"] = self.api_key
        self.client = MemoryClient(api_key=self.api_key)
        self.async_client = AsyncMemoryClient(api_key=self.api_key)
        print(f"🚀 Apex Mem0 Initialized | Account: {key_type}")

    # --- TIER 1: ENTERPRISE (Monitoring) ---
    def system_audit(self):
        print("📊 [Tier 1] System Audit...")
        # Placeholder: Real-world audit would check org/project usage quotas
        return {"status": "ACTIVE", "protocol": "APEX-v2"}

    # --- TIER 2: ADVANCED LOGIC (Search) ---
    def semantic_retrieval(self, query: str, user_id: str):
        """
        [Tier 2] Semantic search using V2 filters.
        """
        print(f"🔍 [Tier 2] Searching: '{query}'")
        # Ensure we provide a valid filter as required by the V2 API
        filters = {"AND": [{"user_id": user_id}]}
        return self.client.search(query=query, filters=filters)

    # --- TIER 3: CONCURRENCY (Async) ---
    async def parallel_ingest(self, items: List[str], user_id: str):
        """
        [Tier 3] High-speed parallel storage.
        """
        print(f"⚡ [Tier 3] Parallel Ingestion for {user_id}...")
        tasks = [
            self.async_client.add(messages=[{"role": "user", "content": item}], user_id=user_id)
            for item in items
        ]
        return await asyncio.gather(*tasks, return_exceptions=True)

    # --- TIER 4: INTEGRATION (Agent Schema) ---
    def agent_tool_schema(self):
        """
        [Tier 4] Schema for LLM tool-calling.
        """
        return {
            "name": "mem0_apex",
            "description": "Fetch long-term user context.",
            "parameters": {"type": "object", "properties": {"query": {"type": "string"}}}
        }

    # --- TIER 5: CORE (CRUD) ---
    def store(self, content: str, user_id: str, metadata: Dict = None):
        return self.client.add(
            messages=[{"role": "user", "content": content}],
            user_id=user_id,
            metadata=metadata or {}
        )

    def fetch_user_history(self, user_id: str):
        return self.client.get_all(filters={"AND": [{"user_id": user_id}]})

async def main():
    apex = ApexMem0Master(key_type="PRIMARY")
    
    # Audit
    print(f"Audit: {apex.system_audit()}")

    # Store
    user = "casey_admin"
    print("\n[Phase 1] Storing...")
    apex.store("High-Class Home Services: Specialized in forensic property restoration.", user)

    # Parallel
    print("\n[Phase 2] Parallel Ingest...")
    await apex.parallel_ingest(["Note A", "Note B"], user)

    # Search
    print("\n[Phase 3] Searching...")
    results = apex.semantic_retrieval("restoration", user)
    print(f"Found {len(results)} results.")

    # Get All
    print("\n[Phase 4] Final Sync...")
    all_data = apex.fetch_user_history(user)
    print(f"Total entries: {len(all_data)}")

if __name__ == "__main__":
    asyncio.run(main())
