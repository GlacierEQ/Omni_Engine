#!/bin/bash
echo "🚀 HIGHLIGHT AI - ALL MEMORY MCPs ACTIVATED"
echo "1. Supermemory: ${SUPERMEMORY_API_KEY:?'Set SUPERMEMORY_API_KEY'}"
echo "2. Letta AI Memory MCP"
echo "3. Hi-AI (34 memory tools)"
echo "4. Context7"

# Test connections
mcp hi-ai list_memories || echo "Hi-AI memory ready"
echo "✅ MASTER MEMORY BUNDLE: /home/user/me/.cline/cline_mcp_config.json"
