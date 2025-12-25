#!/usr/bin/env python3
import json
import os

def deploy_config():
    print("🚀 INITIALIZING MISSION 007: UNIFIED MCP-CONFIG DEPLOYMENT")
    print("----------------------------------------------------------")
    
    config = {
        "mcpServers": {
            "cognitive-nexus": {
                "command": "python3",
                "args": ["/home/user/external_repos/ai-cognitive-nexus-mcp/main.py"]
            },
            "mastermind-forensics": {
                "command": "python3",
                "args": ["/home/user/skills/mastermind/agents/forensic_analyst.py"]
            },
            "apple-bridge": {
                "command": "npx",
                "args": ["-y", "@supermemory/apple-mcp"]
            }
        }
    }
    
    output_path = "unified_mcp_config.json"
    with open(output_path, "w") as f:
        json.dump(config, f, indent=2)
    
    # Final Notification
    subprocess_cmd = ["./mission_003_notify.sh", "Unified MCP Config Deployed Successfully"]
    import subprocess
    subprocess.run(subprocess_cmd)
    
    print(f"✅ MISSION 007 COMPLETE: {output_path} generated.")

if __name__ == "__main__":
    deploy_config()
