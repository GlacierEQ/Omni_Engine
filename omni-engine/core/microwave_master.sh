#!/bin/bash
# Move to workspace root
cd ../../
echo "🔥 [OMNI-CORE] Parallel System Optimization..."

python3 omni-engine/core/mission_004_security.py &
python3 omni-engine/core/mission_006_pattern_audit.py &

wait
echo "✅ [OMNI-CORE] Optimization complete."
