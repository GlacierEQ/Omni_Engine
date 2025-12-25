#!/bin/bash
# Memory System Demo - Practical Examples

echo "🧠 Memory MCPs Demo & Examples"
echo "=============================="
echo ""

# Example 1: Search existing memories in Neo4j
echo "1️⃣ Searching Neo4j Knowledge Graph..."
echo "Query: MCP ecosystem gaps and recommendations"
echo ""

mcp neo4j-knowledge-graph-memory memory_find '{
  "query": "MCP ecosystem",
  "context": "full"
}' 2>&1 | head -30

echo ""
echo "---"
echo ""

# Example 2: Show how to store a new decision
echo "2️⃣ Example: How to store a decision in Neo4j"
echo ""
cat << 'DECISION'
Command structure:
mcp neo4j-knowledge-graph-memory memory_store '{
  "memories": [{
    "name": "Decision: Implement Custom Memory Aggregator",
    "memoryType": "decision",
    "localId": "decision_aggregator",
    "observations": [
      "Decided to build memory aggregator across 4 systems. Rationale: Multiple memory systems without aggregation = fragmented context. Solution: Create unified query interface that searches all 4 and synthesizes results. Expected impact: Better context awareness, faster decision making."
    ],
    "metadata": {
      "date": "2024-01-15",
      "priority": "high",
      "systems_involved": ["neo4j", "letta", "mem0", "supermemory"]
    }
  }],
  "relations": [{
    "from": "decision_aggregator",
    "to": "audit_overview",
    "type": "ADDRESSES",
    "strength": 0.95
  }]
}'
DECISION

echo ""
echo "---"
echo ""

# Example 3: Show Letta usage
echo "3️⃣ Example: Store in Letta (Conversation Memory)"
echo ""
cat << 'LETTA'
For conversation context that persists across sessions:

mcp letta-ai-memory-mcp store_memory '{
  "entity": "user",
  "entity_id": "user_123",
  "memory": {
    "summary": "User prefers Neo4j for complex knowledge, wants unified memory interface",
    "tags": ["memory-systems", "preferences"],
    "relationships": ["neo4j", "letta", "mem0"]
  }
}'
LETTA

echo ""
echo "---"
echo ""

# Example 4: Show Mem0 usage for private data
echo "4️⃣ Example: Store in Mem0 (Private Memory)"
echo ""
cat << 'MEM0'
For sensitive/private data:

mcp mem0-private store_memory '{
  "entity": "app",
  "entity_id": "memory-system-v1",
  "memory": {
    "api_keys": {
      "encrypted": true,
      "services": ["neo4j", "github", "supabase"]
    },
    "status": "initialized"
  }
}'
MEM0

echo ""
echo "---"
echo ""

# Example 5: Show Supermemory usage
echo "5️⃣ Example: Store in Supermemory (Cross-Tool)"
echo ""
cat << 'SUPER'
For sharing with other AI tools (ChatGPT, Cursor, etc.):

First, list projects:
mcp supermemory getProjects '{}'

Then add memory:
mcp supermemory addMemory '{
  "content": "MCP Ecosystem has 35+ servers. Key gaps: Slack integration, project management (Linear/Jira). Strengths: Rich memory systems, excellent reasoning, strong web tools",
  "projectId": "sm_project_main"
}'
SUPER

echo ""
echo "=========================================="
echo "✅ Memory system ready!"
echo ""
echo "Quick reference:"
echo "  Neo4j:      Complex knowledge + relationships"
echo "  Letta:      Conversation context + persistence"
echo "  Mem0:       Private/sensitive data (encrypted)"
echo "  Supermemory: Cross-AI sync"
echo ""
echo "See MEMORY_SYSTEM_GUIDE.md for detailed docs"
echo "=========================================="

