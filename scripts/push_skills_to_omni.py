#!/usr/bin/env python3
"""
Push skills system to glaciereq/Omni_Engine
"""

import json
import subprocess
from pathlib import Path

# Configuration
OWNER = "glaciereq"
REPO = "Omni_Engine"
BRANCH = "main"

# Files to push
FILES_TO_PUSH = [
    {
        "path": "skills/data/SKILLS_50_COMPLETE.json",
        "source": "/home/user/skills/SKILLS_50_COMPLETE.json",
        "message": "Add: 50 expert skills database (508 lines)"
    },
    {
        "path": "skills/data/POWERUPS_EXTENDED.json",
        "source": "/home/user/skills/powerups/POWERUPS_EXTENDED.json",
        "message": "Add: 32 powerup multiplier system (353 lines)"
    },
    {
        "path": "skills/data/FORENSIC_SCHEMA_EXTENDED.json",
        "source": "/home/user/skills/forensics/FORENSIC_SCHEMA_EXTENDED.json",
        "message": "Add: 7 forensic tracking systems with 35+ metrics (387 lines)"
    },
    {
        "path": "skills/tools/skills_orchestrator.py",
        "source": "/home/user/skills/cli/skills_orchestrator.py",
        "message": "Add: Skills orchestrator CLI tool (7 commands, 273 lines)"
    },
    {
        "path": "skills/tools/github_repair_scanner.py",
        "source": "/home/user/skills/tools/github_repair_scanner.py",
        "message": "Add: Repair library scanner (28 repos, 13 categories, 267 lines)"
    },
    {
        "path": "integrations/skills/skills_module.py",
        "source": "/home/user/skills/integrations/skills_module.py",
        "message": "Add: Skills integration module for Omni_Engine"
    }
]

def push_file(target_path: str, source_path: str, message: str) -> bool:
    """Push single file to GitHub"""
    print(f"📤 Pushing: {target_path}")
    
    try:
        # Read source file
        with open(source_path, 'r') as f:
            content = f.read()
        
        print(f"   Size: {len(content)} bytes")
        
        # Build MCP command
        payload = {
            "owner": OWNER,
            "repo": REPO,
            "path": target_path,
            "content": content,
            "message": message,
            "branch": BRANCH
        }
        
        # Call MCP
        cmd = ["mcp", "smithery-ai-github", "create_or_update_file", json.dumps(payload)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   ✅ Success!")
            return True
        else:
            print(f"   ❌ Error: {result.stderr[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def main():
    print("🚀 Skills System Push to glaciereq/Omni_Engine")
    print("=" * 70)
    print()
    
    success_count = 0
    failed_count = 0
    
    for file_spec in FILES_TO_PUSH:
        if push_file(file_spec["path"], file_spec["source"], file_spec["message"]):
            success_count += 1
        else:
            failed_count += 1
        print()
    
    print("=" * 70)
    print(f"📊 Results: {success_count} pushed, {failed_count} failed")
    print()
    
    if failed_count == 0:
        print("✅ All files pushed successfully!")
    else:
        print(f"⚠️  {failed_count} files failed to push")

if __name__ == "__main__":
    main()
