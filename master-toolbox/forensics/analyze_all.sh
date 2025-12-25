#!/bin/bash
# FORENSIC BULK ANALYZER - Production ready pipeline
set -euo pipefail

EVIDENCE_DIR="${1:-evidence}"
mkdir -p "$EVIDENCE_DIR" reports

echo "🚨 FORENSIC ANALYSIS STARTED: $(date)" > reports/chain_of_custody.txt

# 1. Chain of custody (hashes)
find "$EVIDENCE_DIR" -type f -exec sha256sum {} \; >> reports/chain_of_custody.txt

# 2. Bulk metadata + PDF analysis
find "$EVIDENCE_DIR" -type f \\( -name "*.pdf" -o -name "*.jpg" -o -name "*.png" \\) -exec python3 /home/user/skills/forensics/tools/pdf_analyzer.py {} \; > reports/full_report.json

# 3. File carving (if image/disk)
if [[ -f "$EVIDENCE_DIR/disk.img" ]]; then
    foremost -i "$EVIDENCE_DIR/disk.img" -o reports/recovered/
fi

echo "✅ ANALYSIS COMPLETE: reports/ generated"
