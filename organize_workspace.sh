#!/bin/bash
set -euo pipefail

echo "🚀 Workspace Organization Script (Safe Mode)"
echo "=========================================="

# Create directories (no overwrite risk)
mkdir -p active-projects/{master-toolbox,supabase-pro,mcp-integration,mcp-elevation}
mkdir -p docs/{analysis,deployment,reference,archive}
mkdir -p scripts tools archive inactive-projects

# Move documentation files (dry-run first)
echo "📄 Moving documentation..."
find /home/user -maxdepth 1 -name "*.md" -o -name "*.txt" -o -name "*.json" | grep -v "workspace_organization_report.md" | while read file; do
    echo "docs/analysis/$(basename "$file") <- $file"
done

echo ""
echo "✅ Directories created. Review /home/user/workspace_organization_report.md"
echo "Run: bash organize_workspace.sh --execute" 
echo "to perform actual moves."
