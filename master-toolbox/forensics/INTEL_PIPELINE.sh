#!/bin/bash
# INTELLIGENCE PIPELINE v2.0 - Correlated Forensic Analysis
set -euo pipefail

TARGET_DIR="${1:-evidence}"
OUTPUT_DIR="intel_reports"
mkdir -p "$OUTPUT_DIR" "$TARGET_DIR"

echo "🚀 DEEP FORENSIC INTELLIGENCE PIPELINE STARTED: $(date)" > "$OUTPUT_DIR/executive_summary.json"

# 1. MULTI-HASH CHAIN OF CUSTODY
echo '{"chain_of_custody": [' > "$OUTPUT_DIR/hashes.json"
find "$TARGET_DIR" -type f -exec sh -c '
  for algo in sha256 sha1 md5; do
    echo -n "$(cat "$1" | '"$algo"'-sum)" >> "'$OUTPUT_DIR/hashes.json'"
  done' _ {} \;
echo ']}' >> "$OUTPUT_DIR/hashes.json"

# 2. DEEP ANALYSIS CORRELATION
python3 /home/user/skills/forensics/tools/advanced_analyzer.py "$TARGET_DIR"/* > "$OUTPUT_DIR/deep_analysis.json"

# 3. TIMELINE RECONSTRUCTION
fls -r -m / "$TARGET_DIR"/*.img "$TARGET_DIR"/*.dd 2>/dev/null | tee "$OUTPUT_DIR/timeline.txt" | grep -i "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec" > "$OUTPUT_DIR/timeline_events.txt"

# 4. MEMORY FORENSICS (Volatility3)
if command -v volatility3; then
  volatility3 -f "$TARGET_DIR"/*.mem --profile Linux analyze > "$OUTPUT_DIR/memory_forensics.txt"
fi

# 5. CARVING + FUZZY HASHING
foremost -i "$TARGET_DIR"/*.img -o "$OUTPUT_DIR/carved/" 2>/dev/null || true
ssdeep -r "$TARGET_DIR" > "$OUTPUT_DIR/fuzzy_hashes.txt"

echo "✅ INTELLIGENCE PIPELINE COMPLETE - $OUTPUT_DIR/"
