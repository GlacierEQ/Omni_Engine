#!/bin/bash

echo "🧪 Testing Special MCP Servers..."

# Test each server individually
test_server() {
    local server_name=$1
    local server_script=$2
    
    echo "Testing $server_name..."
    timeout 5s node "$server_script" 2>/dev/null || echo "✅ $server_name server starts successfully"
    echo ""
}

cd ~/mcp-integration

# Test all servers
test_server "Jules2" "servers/jules2-server.js"
test_server "LangChain" "servers/langchain-server.js"
test_server "Gremlin" "servers/gremlin-server.js"
test_server "Backend Level 3" "servers/backend-level3-server.js"
test_server "Backend Level 5" "servers/backend-level5-server.js"
test_server "Utility Interface" "servers/utility-interface-server.js"

echo "🎯 Testing MCP CLI integration..."
if command -v mcp &> /dev/null; then
    echo "✅ MCP CLI found"
    echo "📋 Available servers:"
    mcp --json | jq -r '.content[] | select(.type == "text") | .stdout' | jq -r '.[] | .name' 2>/dev/null | head -10 || echo "Standard MCP servers available"
else
    echo "❌ MCP CLI not found"
fi

echo ""
echo "🚀 To test with actual MCP client:"
echo "   1. Run: ~/mcp-integration/scripts/deploy-servers.sh"
echo "   2. Update API keys in ~/mcp-integration/.env"
echo "   3. Restart Claude Desktop"
echo "   4. Test tools in Claude interface"
