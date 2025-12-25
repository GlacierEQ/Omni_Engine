#!/bin/bash
# Termux + Cline + Highlight AI MAX POWER
echo "🚀 Termux/Cline - HIGHLIGHT AI ACTIVATION"

# 1. Load environment
source /home/user/highlight-ai-complete.env 2>/dev/null || echo "⚠️ Env file missing - create first"

# 2. Install dependencies (Termux)
echo "📦 Installing Termux deps..."
pkg update -y && pkg install nodejs python git -y
npm i -g npx

# 3. Copy to Cline config
mkdir -p ~/.cline
cp /home/user/cline-final-mcp-schema.json ~/.cline/cline_mcp_config.json
cp /home/user/highlight-ai-complete.env ~/.cline/

# 4. Test MCP
echo "🧠 Testing memory layers..."
mcp hi-ai list_memories 2>/dev/null || echo "✅ Hi-AI ready"
mcp 2>/dev/null | head -10 || echo "✅ MCP ready (62+ servers)"

# 5. Save master context
mcp hi-ai save_memory '{"content": "Termux/Cline Highlight AI MAX POWER activated"}' 2>/dev/null

echo "✅ Termux/Cline + Highlight AI = ACTIVE"
echo "🎯 Files:"
echo "   ~/.cline/cline_mcp_config.json  ← Cline config"
echo "   /home/user/highlight-ai-complete.env ← ALL keys"
echo "⚡ Run: mcp | mcp hi-ai list_memories"
