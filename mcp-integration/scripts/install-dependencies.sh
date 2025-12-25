#!/bin/bash

echo "🚀 Installing MCP Server Dependencies..."

# Create package.json for MCP servers
cat > ~/mcp-integration/package.json << 'PACKAGEJSON'
{
  "name": "special-mcp-servers",
  "version": "1.0.0",
  "description": "Special MCP servers with operator code integration",
  "main": "index.js",
  "scripts": {
    "start:jules2": "node servers/jules2-server.js",
    "start:langchain": "node servers/langchain-server.js", 
    "start:gremlin": "node servers/gremlin-server.js",
    "start:backend3": "node servers/backend-level3-server.js",
    "start:backend5": "node servers/backend-level5-server.js",
    "start:utility": "node servers/utility-interface-server.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.4.0"
  },
  "keywords": ["mcp", "operator-code", "agent-swarm", "hyper-speed"],
  "author": "Operator Code Integration",
  "license": "MIT"
}
PACKAGEJSON

# Install dependencies
cd ~/mcp-integration
npm install

echo "✅ Dependencies installed successfully!"
echo "📦 MCP servers ready for deployment"
