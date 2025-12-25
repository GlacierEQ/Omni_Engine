#!/bin/bash
# Quick Memory Commands Reference

echo "🧠 Memory MCPs - Quick Commands"
echo "================================"
echo ""

# Function to show command examples
show_commands() {
    cat << 'CMDS'
1. NEO4J - Knowledge Graph Memory
   Store: mcp neo4j-knowledge-graph-memory memory_store '{"memories":[{"name":"...","memoryType":"knowledge","observations":["..."]}]}'
   Search: mcp neo4j-knowledge-graph-memory memory_find '{"query":"..."}'
   Update: mcp neo4j-knowledge-graph-memory memory_modify '{"memoryId":"...","updates":{"observations":["..."]}}'

2. LETTA - Conversation Memory
   Store: mcp letta-ai-memory-mcp store_memory '{"entity":"user","entity_id":"...","memory":{...}}'
   Get: mcp letta-ai-memory-mcp get_memory '{"memory_id":"..."}'
   List: mcp letta-ai-memory-mcp get_memories '{"entity":"user"}'

3. MEM0 - Private Memory (Encrypted)
   Store: mcp mem0-private store_memory '{"entity":"app","entity_id":"...","memory":{...}}'
   List: mcp mem0-private list_memories '{"entity":"app","entity_id":"..."}'
   Get: mcp mem0-private get_memory '{"memory_id":"..."}'
   Delete: mcp mem0-private delete_memory '{"memory_id":"..."}'

4. SUPERMEMORY - Cross-Tool Memory
   Projects: mcp supermemory getProjects '{}'
   Add: mcp supermemory addMemory '{"content":"...","projectId":"sm_project_main"}'
   Search: mcp supermemory search '{"query":"...","projectId":"sm_project_main"}'
   User: mcp supermemory whoAmI '{}'

CMDS
}

# Show usage
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    show_commands
    exit 0
fi

# Display commands
show_commands

echo ""
echo "💡 Pro Tips:"
echo "   • Always search before creating to avoid duplicates"
echo "   • Use Neo4j for complex relationships & decisions"
echo "   • Use Mem0 for secrets & sensitive data"
echo "   • Use Letta for conversation persistence"
echo "   • Use Supermemory to sync across AI tools"
echo ""
echo "📖 Full guide: cat ~/MEMORY_SYSTEM_GUIDE.md"

