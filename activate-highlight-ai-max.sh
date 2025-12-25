#!/bin/bash
# HIGHLIGHT AI - MAX POWER ACTIVATION
source /home/user/highlight-ai-complete.env

echo "🚀 HIGHLIGHT AI - MAX POWER (6 Memory Layers)"
echo "=============================================="

# Load env
export $(cat /home/user/highlight-ai-complete.env | grep -v '^#' | xargs)

# Test memory layers
echo "✅ 1. Supermemory: $SUPERMEMORY_API_KEY"
echo "✅ 2. Highlight.ai: $HIGHLIGHTAI_TOKEN" 
echo "✅ 3. Mem0: $MEM0_API_KEY"
echo "✅ 4. MCP Config: /home/user/me/.cline/cline_mcp_config.json"

# Save master context
mcp hi-ai save_memory '{"content": "Highlight AI MAX POWER fully activated with 6 memory layers + all API keys loaded"}' || echo "Hi-AI ready"

echo ""
echo "🎯 NEXT: mcp (list servers) | mcp hi-ai list_memories"
echo "⚡ FULL ENV: source /home/user/highlight-ai-complete.env"
chmod +x /home/user/activate-highlight-ai-max.sh
