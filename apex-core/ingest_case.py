import asyncio
import json
from engine import ApexMem0Master

async def main():
    apex = ApexMem0Master(key_type="PRIMARY")
    
    print("📖 Reading XTREME MEMORY...")
    with open("/home/user/systemic/xtreme_memory/XTREME MEMORY.txt", "r") as f:
        content = f.read()
    
    # Split content into chunks for ingestion (by sections)
    sections = content.split("---")
    print(f"📦 Found {len(sections)} context sections. Starting Parallel Ingestion...")
    
    # Process in batches to avoid overwhelming
    batch_size = 5
    for i in range(0, len(sections), batch_size):
        batch = sections[i:i+batch_size]
        print(f"⚡ Ingesting batch {i//batch_size + 1}...")
        await apex.parallel_ingest(batch, "casey_admin")
    
    print("✅ Ingestion Complete. Master Toolbox is now case-aware.")

if __name__ == "__main__":
    asyncio.run(main())
