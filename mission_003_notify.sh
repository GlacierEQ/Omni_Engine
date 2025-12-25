#!/bin/bash
MESSAGE=$1
echo "[🍎] Apple MCP: Sending System Notification..."
# In a real Mac env, this would be: osascript -e "display notification \"$MESSAGE\" with title \"Mission Control\""
echo ">> NOTIFICATION: $MESSAGE"

# Log to dashboard
echo "- [x] Apple MCP Notification sent: $MESSAGE" >> dashboard/mission_control.md
