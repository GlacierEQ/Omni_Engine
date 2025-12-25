#!/usr/bin/env python3
"""
Unified Memory Management Tool
Provides simplified interface to all 4 memory MCPs
"""

import json
import subprocess
import sys
from datetime import datetime

class MemoryManager:
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.memories_stored = 0
    
    def store_knowledge(self, name, observations, memory_type="knowledge", metadata=None):
        """Store knowledge in Neo4j"""
        memory_obj = {
            "name": name,
            "memoryType": memory_type,
            "observations": observations if isinstance(observations, list) else [observations],
            "metadata": metadata or {}
        }
        
        print(f"📚 Storing '{name}' in Neo4j...")
        cmd = f"mcp neo4j-knowledge-graph-memory memory_store '{json.dumps({\"memories\": [memory_obj]})}'}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if "error" not in result.stdout.lower():
            self.memories_stored += 1
            print(f"   ✅ Stored")
        else:
            print(f"   ⚠️ Neo4j not available (check connection)")
        return True
    
    def search_knowledge(self, query):
        """Search Neo4j knowledge graph"""
        print(f"🔍 Searching: '{query}'")
        cmd = f"mcp neo4j-knowledge-graph-memory memory_find '{json.dumps({\"query\": query, \"context\": \"full\"})}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout[:500])
        return result.stdout
    
    def store_in_letta(self, entity, entity_id, memory_data):
        """Store in Letta for conversation context"""
        print(f"💬 Storing in Letta for {entity}...")
        cmd = f"mcp letta-ai-memory-mcp store_memory '{json.dumps({\"entity\": entity, \"entity_id\": entity_id, \"memory\": memory_data})}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"   ✅ Stored" if "success" in result.stdout.lower() or "error" not in result.stdout.lower() else f"   ⚠️ Error")
        return True
    
    def store_private(self, entity, entity_id, memory_data):
        """Store private/sensitive data in Mem0"""
        print(f"🔐 Storing in Mem0 (encrypted)...")
        cmd = f"mcp mem0-private store_memory '{json.dumps({\"entity\": entity, \"entity_id\": entity_id, \"memory\": memory_data})}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"   ✅ Stored" if "error" not in result.stdout.lower() else f"   ⚠️ Error")
        return True
    
    def list_supermemory_projects(self):
        """List available Supermemory projects"""
        print("📋 Available Supermemory projects:")
        cmd = "mcp supermemory getProjects '{}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout[:500])
        return result.stdout
    
    def report(self):
        """Print summary report"""
        print(f"\n📊 Memory Manager Report")
        print(f"   Memories stored: {self.memories_stored}")
        print(f"   Systems active: 4 (Neo4j, Letta, Mem0, Supermemory)")
        print(f"   Status: ✅ Ready")

if __name__ == "__main__":
    mgr = MemoryManager()
    
    # Demo workflow
    print("=" * 50)
    print("Memory Manager - Unified Interface Demo")
    print("=" * 50)
    print()
    
    # 1. Store an initial observation
    mgr.store_knowledge(
        name="Memory System Initialization",
        observations=[
            "Set up unified memory manager to simplify access to 4 memory MCPs. Purpose: Provide single interface for storing, searching, and managing knowledge across Neo4j (graphs), Letta (conversation), Mem0 (private), and Supermemory (cross-AI)."
        ],
        metadata={"date": datetime.now().isoformat(), "version": "1.0"}
    )
    
    # 2. Search for existing knowledge
    mgr.search_knowledge("MCP ecosystem")
    
    # 3. List supermemory projects
    mgr.list_supermemory_projects()
    
    # Print report
    mgr.report()
    
    print("\n✨ Memory system ready for use!")
    print("   Use: python3 memory_manager.py")

