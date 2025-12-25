# Supabase Admin MCP - IMMEDIATE POWER COMMANDS

./connect_supabase_admin.sh  # Run first

Then:
```bash
# 1. Analyze your slow queries + indexes needed
mcp supabase-admin analyze_slow_queries

# 2. Get perfect indexes for YOUR schema
mcp supabase-admin recommend_indexes

# 3. Apply them automatically
mcp supabase-admin auto_create_indexes

# 4. Full performance report
mcp supabase-admin performance_metrics
```
