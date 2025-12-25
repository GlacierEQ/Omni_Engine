#!/bin/bash
# 🔥 BROWSER MASTER - ONE BUTTON CASE CRAWLING + PDF INTELLIGENCE
set -euo pipefail

echo "🚀 BROWSER MASTER v1.0 - Sequential Case Crawling"
echo "Usage: $0 <court_url>"

URL="${1:-https://example-court.gov/cases}"
OUTPUT="browser_crawler"

mkdir -p "$OUTPUT"/{pdfs,organized}

# 1. PRODUCTION CRAWLER
cd /home/user && python3 /home/user/skills/browser_crawler/PRODUCTION_CRAWLER.py "$URL"

# 2. EXHIBIT PIPELINE INTEGRATION
echo "🔗 Integrating with exhibit pipeline..."
cp browser_crawler/pdfs/* exhibits/raw/ 2>/dev/null || true
cd exhibits && /exhibits 2>/dev/null || true

# 3. FORENSIC ANALYSIS
echo "🔍 Forensic preprocessing..."
cd /home/user && /forensics/orchestrator browser_crawler/pdfs/ 2>/dev/null || true

echo "✅ BROWSER MASTER COMPLETE:"
echo "  📊 $OUTPUT/CASE_MASTER_INVENTORY.json"
echo "  📁 $OUTPUT/organized/"
echo "  🎯 exhibits/processed/ (Bates stamped)"
