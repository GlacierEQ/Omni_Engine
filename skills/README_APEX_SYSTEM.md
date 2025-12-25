# 🧠 README: APEX SYSTEM ARCHITECTURE

## Overview
The Apex System is a bridge between **Local Skills** (files, workflows, templates) and **Cloud Capabilities** (MCP servers).

## Architecture
1. **Orchestration Layer**: `apex_orchestrator.py`
   - Manages environment variables in `.env.apex`.
   - Generates the `mcp_universal_config.json`.
   
2. **Intelligence Layer**: `~/skills/`
   - Contains the 57 core skills.
   - Domain deep-dives for strategic decision making.
   
3. **Connectivity Layer**: 69 MCP Servers
   - Real-time access to your external tools (GitHub, Slack, Notion).

## Governance
The system follows the **System Integrity Protocol**, ensuring that the AI remains an executor while you remain the strategist.
