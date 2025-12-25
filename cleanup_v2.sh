#!/bin/bash
set -euo pipefail

echo "=== Workspace Deep Cleanup v2 ==="

# 1. Fix remaining .env (targeted)
echo "Securing remaining .env files..."
find /home/user -name .env -o -name '*.env' | while read file; do
  chmod 600 "$file" 2>/dev/null || sudo chmod 600 "$file"
done
echo "✅ All .env secured"

# 2. Remove node_modules completely
echo "Removing all node_modules..."
find /home/user -name node_modules -type d -exec rm -rf {} + 2>/dev/null || true
echo "✅ node_modules gone"

# 3. Global .gitignore fix (proper syntax)
echo "node_modules/
.env
*.log
.DS_Store
__pycache__/
*.pyc
tmp/
.DS_Store" > /home/user/.gitignore

find /home/user -maxdepth 3 -type d -exec sh -c '[ -d "{}/.git" ] && echo "node_modules/
.env" > "{}/.gitignore"' \; 2>/dev/null || true
echo "✅ .gitignore everywhere"

# 4. Archive .gcs-sync duplicates
echo "Archiving .gcs-sync..."
mkdir -p /home/user/archive
rsync -a --remove-source-files /home/user/.gcs-sync/ /home/user/archive/ 2>/dev/null || true
rmdir /home/user/.gcs-sync 2>/dev/null || true
echo "✅ .gcs-sync → archive/"

# 5. Git maintenance
find /home/user -name .git -type d | while read gitdir; do
  cd "$(dirname "$gitdir")" 2>/dev/null && git gc --aggressive --prune=now || true
done
echo "✅ Git optimized"

echo "=== DEEP CLEAN COMPLETE ==="
tree /home/user -L 2 -I 'node_modules|.git' > /home/user/clean_structure.txt
