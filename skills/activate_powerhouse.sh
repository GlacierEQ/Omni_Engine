#!/bin/bash
# 🚀 MCP POWERHOUSE ACTIVATION SCRIPT

echo "=========================================="
echo "   MCP POWERHOUSE SYSTEM ACTIVATION      "
echo "=========================================="

# 1. Check Python dependencies
echo "🔍 Checking dependencies..."
pip install -q requests pandas > /dev/null 2>&1

# 2. Run Health Check
echo "🔍 Auditing MCP Servers..."
python3 -c "
import subprocess, json
servers = ['github', 'notion', 'exa', 'filesystem', 'google-docs']
for s in servers:
    res = subprocess.run(['mcp', s], capture_output=True, text=True)
    status = '✅ READY' if res.returncode == 0 else '❌ ISSUE'
    print(f'  {s:<15} : {status}')
"

# 3. Initialize Skills
echo "🔍 Initializing Skills Manifest..."
python3 /home/user/skills/cli/skills.py list --domain strategy > /dev/null

# 4. Final Status
echo "=========================================="
echo "🟢 POWERHOUSE SYSTEM IS ACTIVE"
echo "Copy-Paste this for your AI Team:"
echo "'I am operating within the MCP Powerhouse. System Protocol at ~/skills/UNIVERSAL_AI_TEAM_PROTOCOL.md'"
echo "=========================================="
