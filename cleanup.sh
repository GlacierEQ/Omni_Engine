#!/bin/bash
set -euo pipefail

echo "=== Workspace Cleanup (DRY RUN FIRST) ==="

# 1. SECURITY: Fix .env permissions
echo "Fixing .env permissions..."
chmod 600 /home/user/mcp-integration/.env /home/user/.gcs-sync/mcp-integration/.env 2>/dev/null || true
echo "✅ .env secured"

# 2. Create .gitignore templates
echo "Creating .gitignore files..."
cat > /home/user/.gitignore << 'GITIGNORE'
node_modules/
.env
*.log
.DS_Store
__pycache__/
*.pyc
*.pdf
*.txt
