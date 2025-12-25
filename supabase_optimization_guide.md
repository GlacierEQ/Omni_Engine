# Supabase Index Optimization Guide

## 1. Identify Slow Queries
Run in Supabase SQL Editor:
```sql
SELECT 
  query,
  calls,
  total_exec_time / calls as avg_time,
  total_exec_time
FROM pg_stat_statements 
ORDER BY total_exec_time DESC 
LIMIT 20;
```

## 2. Common Index Patterns
### High-Cardinality WHERE clauses
```sql
-- For user lookups
CREATE INDEX idx_users_email ON public.users(email);

-- For filtering by status + date
CREATE INDEX idx_orders_status_created ON public.orders(status, created_at);
```

### JOIN performance
```sql
-- Foreign key indexes (automatic in Supabase but verify)
CREATE INDEX idx_comments_post_id ON public.comments(post_id);
```

### Composite indexes for frequent query patterns
```sql
-- Dashboard queries: user + recent activity
CREATE INDEX CONCURRENTLY idx_user_activity 
ON public.activity(user_id, created_at DESC) 
WHERE deleted_at IS NULL;
```

## 3. Query Analysis Checklist
```
☐ Added LIMIT for pagination
☐ Used exact matches before range scans  
☐ Composite index covers SELECT + WHERE + ORDER BY
☐ Partial indexes for common filters (status='active')
☐ GIN for JSONB / array searches
```

## 4. Supabase-Specific Optimizations
```sql
-- pg_trgm for fuzzy search
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_products_name_trgm ON products USING gin(name gin_trgm_ops);

-- Vector indexes (pgvector)
CREATE INDEX idx_embeddings ON embeddings USING ivfflat(embedding vector_cosine_ops);
```

## 5. Monitoring & Maintenance
```sql
-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes ORDER BY idx_scan DESC;

-- Bloat analysis
SELECT * FROM pgstattuple('tablename');
```

**Next Steps:**
1. Share your slow query logs from pg_stat_statements
2. List your main tables + common WHERE/JOIN patterns
3. Point to your Supabase project schema files

