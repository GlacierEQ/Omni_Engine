#!/bin/bash
echo "=== GLACIER-REPAIR-OMNIBUS MCP Status ==="
curl -s http://localhost:8081/health || echo "mem0: DOWN"
curl -s http://localhost:8082/health || echo "supermemory: DOWN"  
curl -s http://localhost:8083/health || echo "stealth_microwave: DOWN"
mcp
