import asyncio
import json
from engine import ApexMem0Master

async def main():
    apex = ApexMem0Master(key_type="PRIMARY")
    print("\n--- [APEX] Querying Motion to Stay Context ---")
    results = apex.semantic_retrieval("Motion to Stay", "casey_admin")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
