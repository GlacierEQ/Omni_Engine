#!/bin/bash

echo "🚀 Master Toolbox v2.0 - Startup"
echo "=================================="

cd "$(dirname "$0")/.."

echo "✅ Directory: $(pwd)"
echo "✅ Config: $(pwd)/core/config.json exists"

# Initialize systems
python3 core/toolbox.py start

echo ""
echo "📝 Next Steps:"
echo "   1. python3 core/toolbox.py status          # Check status"
echo "   2. python3 core/toolbox.py process <file>  # Process evidence"
echo "   3. python3 core/toolbox.py monitor         # Start monitoring"
