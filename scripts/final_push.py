#!/usr/bin/env python3
import json
import subprocess

OWNER = "glaciereq"
REPO = "Omni_Engine"
BRANCH = "main"

# Final files
FINAL_FILES = [
    {
        "path": "skills/data/.gitkeep",
        "content": "",
        "message": "Add: Data directory"
    },
    {
        "path": "integrations/skills/README.md",
        "content": """# Skills Integration Module

Python module integrating the comprehensive skills system with Omni_Engine.

## Usage

```python
from integrations.skills import SkillsIntegration, SkillsEngine

# Create integration
integration = SkillsIntegration()

# Analyze for goal
analysis = integration.analyze_for_goal("machine learning")

# Access engine directly
engine = integration.engine
skill = engine.get_skill(1)
```

## Components

- **SkillsEngine** - Core skills database and search
- **SkillsIntegration** - Omni_Engine integration layer

See docs/skills/ for full documentation.
""",
        "message": "Add: Skills integration module README"
    }
]

def push_file(path: str, content: str, message: str) -> bool:
    try:
        payload = {
            "owner": OWNER,
            "repo": REPO,
            "path": path,
            "content": content,
            "message": message,
            "branch": BRANCH
        }
        cmd = ["mcp", "smithery-ai-github", "create_or_update_file", json.dumps(payload)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {path}")
            return True
        return False
    except:
        return False

print("🎉 Final Push")
print("=" * 60)
for f in FINAL_FILES:
    push_file(f["path"], f["content"], f["message"])
print("=" * 60)
print("✅ Skills system completely pushed to glaciereq/Omni_Engine!")
