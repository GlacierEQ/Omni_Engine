#!/bin/bash
set -euo pipefail

echo "🌋 FULL GLACIEREQ PIPELINE: FILEBOSS → SUPERLUMINAL_MATRIX"
echo "========================================================"

# Phase 1: FILEBOSS Organization
echo "📁 PHASE 1: ULTIMATE_FILEBOSS..."
python3 /home/user/ULTIMATE_FILEBOSS.py /home/user -o /home/user/organized

# Phase 2: SUPERLUMINAL CASE MATRIX
echo ""
echo "🔗 PHASE 2: ULTIMATE_SUPERLUMINAL_MATRIX..."
python3 /home/user/ULTIMATE_SUPERLUMINAL_MATRIX.py --exhibits organized --case GLACIEREQ-001

echo ""
echo "✅ PIPELINE COMPLETE! Outputs:"
echo "   organized/FILEBOSS_INVENTORY.json"
echo "   organized/CASE_MATRIX_GLACIEREQ-001.json"
echo "   organized/CASE_MATRIX_GLACIEREQ-001.md"
