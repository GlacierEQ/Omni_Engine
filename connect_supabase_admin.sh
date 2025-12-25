#!/bin/bash
# 🔥 SUPABASE ADMIN MCP CONNECTOR - TOTAL CONTROL

echo "🚀 Supabase Admin MCP Connector"
echo "================================"

# Get Supabase credentials
read -p "Supabase Project URL (https://*.supabase.co): " SUPABASE_URL
read -p "Service Role Key (Dashboard > Settings > API): " SUPABASE_SERVICE_ROLE_KEY
read -s -p "Anon Key (optional): " SUPABASE_ANON_KEY && echo

# Test connection
echo "🔍 Testing Supabase connection..."
curl -s -X POST "$SUPABASE_URL/rest/v1/rpc/ping" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  | grep -q '"ok"' && echo "✅ Connection OK" || echo "❌ Connection failed"

# Export for MCP
export SUPABASE_URL
export SUPABASE_SERVICE_ROLE_KEY
[ -n "$SUPABASE_ANON_KEY" ] && export SUPABASE_ANON_KEY

echo "🔗 Connecting Supabase Admin MCP..."
mcp abdqum/supabase-mcp-selfhosted

echo "✅ Run these for index optimization:"
echo "  mcp supabase-admin analyze_slow_queries"
echo "  mcp supabase-admin recommend_indexes"
