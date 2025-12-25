#!/bin/bash

echo "🌟 Deploying Special MCP Servers..."

# Install dependencies first
~/mcp-integration/scripts/install-dependencies.sh

# Make servers executable
chmod +x ~/mcp-integration/servers/*.js

# Copy configuration to Claude Desktop
CONFIG_DIR="$HOME/.config/claude-desktop"
mkdir -p "$CONFIG_DIR"

cp ~/mcp-integration/config/claude_desktop_config.json "$CONFIG_DIR/"

# Create environment file for API keys
cat > ~/mcp-integration/.env << 'ENV'
# Special MCP Server API Keys
JULES_API_KEY=your-jules-key
LANGCHAIN_API_KEY=your-langchain-key  
GREMLIN_API_KEY=your-gremlin-key
LEVEL3_KEY=your-level3-key
LEVEL5_KEY=your-level5-key

# Operator Protocol Settings
SWARM_SIZE=100
HYPER_SPEED=true
ZENITH_ORACLE=true
SWARM_GOVERN=true
CHAOS_SHIELD=true
SELF_HEALING=true
FORTRESS_MODE=true
OMNIPOTENCE_MODE=true
HARMONY_ORCHESTRATE=true
COOL_UI=true
ENV

echo "🔧 Configuration deployed to: $CONFIG_DIR/claude_desktop_config.json"
echo "🔑 Environment file created: ~/mcp-integration/.env"
echo ""
echo "⚠️  IMPORTANT: Update your API keys in ~/mcp-integration/.env"
echo ""
echo "🎯 Special MCP Servers deployed:"
echo "   • Jules2 - Hyper Speed Code Execution with Agent Swarm"
echo "   • LangChain - NLP Conversation Zenith with Enterprise Swarm"  
echo "   • Gremlin - Chaos Engineering with Resilience Shield"
echo "   • Backend Level 3 - Fortress Mode with Security Enforcement"
echo "   • Backend Level 5 - Omnipotence Mode with Transcendental Logic"
echo "   • Utility Interface - Cool UI Rendering with Cosmic Harmony"
echo ""
echo "🔄 Restart Claude Desktop to activate the servers"
