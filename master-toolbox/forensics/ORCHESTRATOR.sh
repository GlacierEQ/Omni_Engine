#!/bin/bash
# ULTIMATE FORENSIC ORCHESTRATOR v3.0 - AI + Deep Tools Pipeline
set -euo pipefail

EVIDENCE="${1:-evidence}"
INTEL="forensic_intel"
mkdir -p "$INTEL"

echo "🧠 ULTIMATE FORENSIC ORCHESTRATOR v3.0"
echo "Target: $EVIDENCE → Output: $INTEL/"

# PHASE 1: Chain of Custody + Deep Hashes
echo '["chain_of_custody"]' > "$INTEL"/custody.json
find "$EVIDENCE" -type f -exec sha256sum {} \; -exec sha1sum {} \; -exec md5sum {} \; >> "$INTEL"/custody_raw.txt

# PHASE 2: Tool Correlation Matrix
python3 /home/user/skills/forensics/tools/advanced_analyzer.py "$EVIDENCE"/* > "$INTEL"/deep_scan.json 2>/dev/null || true

# PHASE 3: AI Intelligence Layer
if [ -f /home/user/skills/forensics/ai/FORENSIC_AGENT.py ]; then
    python3 /home/user/skills/forensics/ai/FORENSIC_AGENT.py > "$INTEL"/ai_assessment.json
fi

# PHASE 4: Timeline + Carving
fls -r -m / "$EVIDENCE"/*.img 2>/dev/null | tee "$INTEL"/timeline_raw.txt | head -100 > "$INTEL"/timeline.txt
foremost -i "$EVIDENCE"/*.img -o "$INTEL"/carved/ 2>/dev/null || true

# PHASE 5: MCP Integration Check
echo "MCP Status:" >> "$INTEL"/executive_summary.md
mcp | grep -i "file\|pdf\|extractor\|forensic" >> "$INTEL"/executive_summary.md || echo "No forensic MCPs detected" >> "$INTEL"/executive_summary.md

echo "✅ ORCHESTRATOR COMPLETE: $INTEL/"
echo "**INTELLIGENCE GENERATED:** $(ls -la $INTEL/ | wc -l) artifacts"
