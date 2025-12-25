# Supabase MCP Setup (Most Powerful Option)

## 1. Connect Official Supabase Server
```
mcp 2b4dcd79-3e14-4e72-8fdd-9dc90cfbbe4a
```
**Tools include:** Docs search, project management, migrations, performance monitoring

## 2. Self-Hosted Power Option (Full Admin)
Server: `abdqum/supabase-mcp-selfhosted`
```
# Common connection issues + fixes:
1. Check Supabase project URL + anon key
2. Verify self-hosted server running
3. Use UI Apps panel to authenticate OAuth
```

## 3. Quickstart Powerful Queries
Once connected:
```bash
# Analyze slow queries + recommend indexes
mcp supabase analyze_performance

# Generate optimal indexes for your schema
mcp supabase generate_indexes

# Monitor real-time query performance
mcp supabase query_analyzer
```

## 4. Fallback: Direct Supabase CLI
```bash
npm install -g supabase
supabase init
supabase db pull  # Get current schema
supabase db diff  # Analyze missing indexes
```

**Action Required:** Run `mcp 2b4dcd79-3e14-4e72-8fdd-9dc90cfbbe4a` and share your Supabase project URL for targeted setup.

