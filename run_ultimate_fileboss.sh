#!/bin/bash
set -euo pipefail

echo "🚀 ULTIMATE_FILEBOSS - Merging glaciereq logic + Workspace cleanup"
echo "====================================================================="

# Dry run first
echo "🐱 1. DRY RUN (Preview duplicates + plan)..."
python3 /home/user/ULTIMATE_FILEBOSS.py /home/user --dry-run

echo ""
echo "📊 2. FULL ORGANIZATION (creates /home/user/organized/)..."
echo "This will:"
echo "   ✅ Remove duplicates (moves to archive/)"
echo "   ✅ Categorize files (docs/, scripts/, configs/, evidence/)"
echo "   ✅ Bates stamp everything"
echo "   ✅ Generate FILEBOSS_INVENTORY.json"
echo ""
read -p "Approve? (y/N): " APPROVE

if [[ $APPROVE =~ ^[Yy] ]]; then
    python3 /home/user/ULTIMATE_FILEBOSS.py /home/user -o /home/user/organized
    echo "✅ Complete! Check /home/user/organized/FILEBOSS_INVENTORY.json"
else
    echo "👋 Aborted. Run manually: python3 ULTIMATE_FILEBOSS.py --help"
fi
