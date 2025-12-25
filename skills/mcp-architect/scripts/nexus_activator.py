#!/usr/bin/env python3
import json
import os

def generate_cline_config():
    registry_path = "skills/mcp-architect/registry/master_registry.json"
    with open(registry_path, "r") as f:
        registry = json.load(f)
    
    cline_config = {
        "mcpServers": {}
    }
    
    for name, data in registry["endpoints"].items():
        if data["type"] == "python":
            cline_config["mcpServers"][name] = {
                "command": "python3",
                "args": [os.path.abspath(data.get("path", ""))]
            }
        elif data["type"] == "node":
            cline_config["mcpServers"][name] = {
                "command": data["command"],
                "args": data["args"]
            }
            
    output_path = "mcp_universal_config.json"
    with open(output_path, "w") as f:
        json.dump(cline_config, f, indent=2)
        
    return f"Universal MCP configuration generated at {output_path}"

if __name__ == "__main__":
    print(generate_cline_config())
