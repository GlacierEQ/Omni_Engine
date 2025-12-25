#!/bin/bash
# 🚀 Supabase Pro Full Deploy

echo "🛫 Deploying Supabase Pro E2E..."

# 1. Apply migrations
echo "📊 Applying migrations..."
mcp 2b4dcd79-3e14-4e72-8fdd-9dc90cfbbe4a apply_migrations '{"project_ref": "YOUR_PROJECT_REF"}'

# 2. Deploy Edge Functions
echo "⚡ Deploying Edge Functions..."
mcp 2b4dcd79-3e14-4e72-8fdd-9dc90cfbbe4a deploy_functions '{"project_ref": "YOUR_PROJECT_REF"}'

# 3. Frontend deploy (Vercel/Netlify)
echo "🌐 Deploying Frontend..."
npm run build --prefix frontend
# Add your CDN deploy here

echo "✅ Deploy COMPLETE"
