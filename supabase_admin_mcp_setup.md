# Supabase Admin MCP - TOTAL CONTROL SETUP

## 🎯 Most Powerful: Self-Hosted Admin Server
**Server:** `abdqum/supabase-mcp-selfhosted`

## 1. Prerequisites
```
# Get from Supabase Dashboard → Settings → API
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key  # 👈 ADMIN KEY
```

## 2. Connect via UI (Recommended)
1. **Apps Panel** → Search "Supabase Admin" 
2. Select `@abdqum/supabase-mcp-selfhosted`
3. **Paste these env vars:**
```
SUPABASE_URL=your-project-url
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

## 3. CLI Connection (Advanced)
```
# Set environment variables
export SUPABASE_URL=https://your-project.supabase.co
export SUPABASE_SERVICE_ROLE_KEY=eyJ...

# Connect server
mcp abdqum/supabase-mcp-selfhosted
```

## 4. Admin Power Tools (Once Connected)
```bash
# 🔥 PERFECT FOR YOUR INDEX OPTIMIZATION
mcp supabase-admin analyze_slow_queries
mcp supabase-admin recommend_indexes  
mcp supabase-admin auto_create_indexes

# Full control commands
mcp supabase-admin generate_schema_types
mcp supabase-admin performance_metrics
mcp supabase-admin row_level_security_audit
mcp supabase-admin realtime_subscribe_test
```

## 5. Troubleshooting Connection
```
# Test direct connection first
curl -X POST $SUPABASE_URL/rest/v1/rpc/ping \\
  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY"

# Check MCP logs
mcp abdqum/supabase-mcp-selfhosted --debug
```

## 🚀 Next Steps
1. **Share your Supabase project URL** 
2. **Copy service role key** from Dashboard → Settings → API
3. **Use Apps panel** → Search "Supabase Admin" → Connect

**This gives TOTAL CONTROL** - schema changes, RLS policies, performance tuning, realtime monitoring.

