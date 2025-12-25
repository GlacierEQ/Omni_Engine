#!/usr/bin/env bash
cd /home/user || exit 1
echo "--- SYSTEM STATUS REPORT ---"
echo "PWD=$(pwd)"
echo "DATE=$(date)"
echo ""
echo "--- MCP REGISTRY (Page 1) ---"
mcp --page 1 || true
echo ""
echo "--- NOTION CANONICAL CHECK ---"
mcp notion || true
echo ""
echo "--- POWERHOUSE TOOLBOX HEALTH ---"
cd /home/user/master-toolbox && export PYTHONPATH=$PYTHONPATH:/home/user/master-toolbox && python3 core/toolbox.py health || true
echo ""
echo "--- AUDIT LOG TAIL ---"
tail -n 5 /home/user/master-toolbox/logs/apex_audit.jsonl 2>/dev/null || echo "No audit log found yet."
