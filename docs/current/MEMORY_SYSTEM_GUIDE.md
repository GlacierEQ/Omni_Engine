# Memory MCPs Utilization Guide

## 🧠 Your Connected Memory Systems

### 1. **Neo4j Knowledge Graph Memory** (Recommended for Complex Knowledge)
**Use for:** Structured knowledge, relationships, decision contexts, technical architectures

**Key Features:**
- Knowledge graph with semantic relationships
- Memory types: knowledge, decision, issue, implementation, architecture, pattern, insight
- Search patterns: text, IDs, temporal filters
- Relationship strengths (0.1-1.0 importance)

**Commands:**
```bash
# Store memories with relationships
mcp neo4j-knowledge-graph-memory memory_store '<json>'

# Search memories
mcp neo4j-knowledge-graph-memory memory_find '<json>'

# Modify/update existing memories
mcp neo4j-knowledge-graph-memory memory_modify '<json>'

# Switch database context
mcp neo4j-knowledge-graph-memory database_switch '<json>'
```

**Example - Store a decision:**
```json
{
  "memories": [{
    "name": "Decision: Add Slack Integration",
    "memoryType": "decision",
    "observations": [
      "Decided to prioritize Slack integration as top gap in current ecosystem. Reason: 35+ servers but no team communication. Impact: Will improve team coordination workflows."
    ],
    "metadata": {"date": "2024-01-15", "priority": "high"}
  }]
}
```

---

### 2. **Letta AI Memory** (Best for Conversation Context)
**Use for:** Conversation history, user preferences, ongoing context

**Key Features:**
- Maintains session persistence
- User/agent/app/run specific memories
- Automatic context recall

**Commands:**
```bash
# List memories for an entity
mcp letta-ai-memory-mcp get_memories '<json>'

# Store a memory
mcp letta-ai-memory-mcp store_memory '<json>'

# Get single memory
mcp letta-ai-memory-mcp get_memory '<json>'

# Update memory
mcp letta-ai-memory-mcp update_memory '<json>'
```

---

### 3. **Mem0 Private Memory** (For Private Data)
**Use for:** Sensitive personal data, API keys (encrypted), private configurations

**Key Features:**
- Private encryption
- User/agent/app/run organization
- Cascade deletion support

**Commands:**
```bash
# List all memories
mcp mem0-private list_memories '<json>'

# Store private memory
mcp mem0-private store_memory '<json>'

# Get specific memory
mcp mem0-private get_memory '<json>'

# Delete memory (with confirmation)
mcp mem0-private delete_memory '<json>'
```

---

### 4. **Supermemory** (Universal Cross-AI Memory)
**Use for:** Shared memory across Claude, ChatGPT, Cursor, other AI tools

**Key Features:**
- Project-based organization
- Semantic search
- Cross-platform synchronization

**Commands:**
```bash
# Add memory to project
mcp supermemory addMemory '<json>'

# Search memories
mcp supermemory search '<json>'

# List available projects
mcp supermemory getProjects '<json>'

# Get current user info
mcp supermemory whoAmI '<json>'
```

---

## 📋 Recommended Usage Patterns

### Pattern 1: Project Setup
```
1. Use Neo4j to store project architecture & decisions
2. Use Mem0 for project-specific credentials
3. Use Supermemory to sync across tools
4. Use Letta for ongoing conversation context
```

### Pattern 2: Knowledge Capture
```
1. Discover knowledge (via web search with Exa)
2. Store in Neo4j with observations
3. Link related concepts with relationships
4. Search to inform future decisions
```

### Pattern 3: Long-term Learning
```
1. Experience/outcome happens
2. Letta captures in conversation
3. Neo4j stores as insight/pattern
4. Mem0 keeps private notes
5. Supermemory syncs to other tools
```

---

## 🔍 Search Examples

### Neo4j Graph Search
```json
{
  "query": "integration strategy",
  "context": "full",
  "graphMode": {
    "traverseFrom": ["audit_overview"],
    "depth": 2,
    "returnContext": "relations"
  }
}
```

### Supermemory Search
```json
{
  "query": "MCP ecosystem gaps",
  "projectId": "sm_project_main"
}
```

---

## 💾 Current Stored Data

✅ **Already in Neo4j:**
- MCP Ecosystem Audit Overview
- Memory Systems Available
- Relationships between audit findings and memory systems

---

## 🚀 Next Actions

1. **Store Project Context** - Use Neo4j to document current projects
2. **Capture Decisions** - Every decision → Neo4j memory
3. **Link Knowledge** - Create relationships between concepts
4. **Sync Cross-Platform** - Add key memories to Supermemory projects
5. **Guard Secrets** - Store credentials/configs in Mem0-Private

---

## ⚙️ Management

**List all memory MCPs:**
```bash
mcp neo4j-knowledge-graph-memory database_switch '{"database":"main"}'
mcp letta-ai-memory-mcp get_memories '{"entity":"user"}'
mcp mem0-private list_memories '{}'
mcp supermemory getProjects '{}'
```

**Query all Neo4j memories:**
```bash
mcp neo4j-knowledge-graph-memory memory_find '{"query":"*"}'
```

**Clean up old memories (Mem0):**
```bash
# First list, then delete with ID
mcp mem0-private delete_memory '{"memory_id":"<id>"}'
```

---

## 🎯 Best Practices

✅ **Do:**
- Search before creating to avoid duplicates
- Use specific names with searchable keywords
- Add rich metadata for filtering
- Link related concepts with relationships
- Use appropriate memory types
- Document decisions with impact

❌ **Don't:**
- Store same info in multiple systems
- Use vague memory names
- Skip relationships
- Forget to search first
- Mix sensitive data in Neo4j (use Mem0)
- Exceed 50 memories/200 relations per Neo4j request

