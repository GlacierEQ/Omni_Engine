#!/usr/bin/env python3
"""Push documentation and init files to Omni_Engine"""

import json
import subprocess

OWNER = "glaciereq"
REPO = "Omni_Engine"
BRANCH = "main"

# Init files
INIT_FILES = [
    {
        "path": "skills/tools/__init__.py",
        "content": '"""Skills tools module"""\nfrom .skills_orchestrator import SkillsOrchestrator\n\n__all__ = ["SkillsOrchestrator"]\n',
        "message": "Add: Skills tools init"
    },
    {
        "path": "integrations/skills/__init__.py",
        "content": '"""Skills integration module"""\nfrom .skills_module import SkillsEngine, SkillsIntegration, integrate_with_omni\n\n__all__ = ["SkillsEngine", "SkillsIntegration", "integrate_with_omni"]\n',
        "message": "Add: Skills integration init"
    }
]

# Documentation files
DOC_FILES = [
    {
        "path": "skills/README.md",
        "content": """# 🎯 Skills System for Omni_Engine

Complete professional skills framework with 50 expert skills, 32 power multipliers, and comprehensive tracking.

## Quick Start

```python
from integrations.skills import SkillsIntegration

skills = SkillsIntegration()
stats = skills.engine.get_system_stats()
print(stats)
```

## Features

- **50 Expert Skills** across 19 categories
- **32 Powerup Multipliers** (2-20x boost)
- **7 Forensic Tracking Systems** (35+ metrics)
- **CLI Tools** for exploration and scanning
- **28 Repair Repositories** organized and tagged

## Usage

### List All Skills
```bash
python -m skills.tools.skills_orchestrator list
```

### Search Skills
```bash
python -m skills.tools.skills_orchestrator search "AI"
```

### Create Execution Plan
```bash
python -m skills.tools.skills_orchestrator plan 12
```

## Files

- `data/` - Skill definitions, powerups, forensics
- `tools/` - CLI tools and utilities
- `../integrations/skills/` - Omni_Engine integration

## Documentation

- See `INTEGRATION.md` for Omni_Engine integration details
- See `API.md` for API reference
- See `USAGE_EXAMPLES.md` for practical examples

---

**Ready to transform potential into exponential results!** 🚀
""",
        "message": "Add: Skills system README"
    },
    {
        "path": "docs/skills/INTEGRATION.md",
        "content": """# Skills System Integration Guide

## Integrating with Omni_Engine

### Import the Module

```python
from integrations.skills import SkillsIntegration, SkillsEngine

# Initialize
skills = SkillsIntegration()
engine = SkillsEngine()
```

### Access Skills

```python
# Get a specific skill
skill = engine.get_skill(1)

# Search for skills
results = engine.search_skills("AI")

# Get system stats
stats = engine.get_system_stats()
```

### Use in Workflows

```python
# Analyze goal
analysis = skills.analyze_for_goal("learn machine learning")

# Get recommended skills and powerups
for skill in analysis["matching_skills"]:
    print(f"{skill['name']}: {skill['description']}")
```

## Directory Structure

```
omni-engine/
├── skills/
│   ├── data/
│   │   ├── SKILLS_50_COMPLETE.json
│   │   ├── POWERUPS_EXTENDED.json
│   │   └── FORENSIC_SCHEMA_EXTENDED.json
│   ├── tools/
│   │   ├── skills_orchestrator.py
│   │   └── github_repair_scanner.py
│   └── README.md
└── integrations/skills/
    ├── skills_module.py
    └── __init__.py
```

## Features

- **50 Skills** - Complete professional skill set
- **32 Powerups** - Productivity multipliers
- **7 Metrics Systems** - Comprehensive tracking
- **CLI Tools** - Exploration and scanning
- **Zero Dependencies** - Self-contained system

---

See README.md for quick start and usage examples.
""",
        "message": "Add: Skills integration documentation"
    },
    {
        "path": "docs/skills/API.md",
        "content": """# Skills System API Reference

## SkillsEngine Class

### Methods

#### `get_skill(skill_id: int) -> Optional[Dict]`
Get a specific skill by ID.

```python
skill = engine.get_skill(1)  # Returns Data Analyst Pro
```

#### `search_skills(query: str) -> List[Dict]`
Search skills by name or description.

```python
results = engine.search_skills("database")
```

#### `list_categories() -> List[str]`
Get all skill categories.

```python
categories = engine.list_categories()
```

#### `get_system_stats() -> Dict`
Get system statistics.

```python
stats = engine.get_system_stats()
# Returns: {
#   "total_skills": 50,
#   "total_powerups": 32,
#   "categories": 19,
#   "forensic_systems": 7
# }
```

## SkillsIntegration Class

### Methods

#### `analyze_for_goal(goal: str) -> Dict`
Find skills relevant to a goal.

```python
analysis = integration.analyze_for_goal("AI/ML")
# Returns matching skills with recommendations
```

## Skill Structure

```json
{
  "id": 1,
  "name": "Data Analyst Pro",
  "category": "Data & Analytics",
  "level": "Expert",
  "description": "...",
  "capabilities": [...],
  "technologies": [...],
  "use_cases": [...]
}
```

---

See USAGE_EXAMPLES.md for practical examples.
""",
        "message": "Add: Skills API documentation"
    }
]

def push_file(path: str, content: str, message: str) -> bool:
    """Push file to GitHub"""
    print(f"📤 Pushing: {path}")
    
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
            print(f"   ✅ Success! ({len(content)} bytes)")
            return True
        else:
            print(f"   ❌ Error")
            return False
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False

def main():
    print("📚 Pushing Documentation & Init Files")
    print("=" * 70)
    print()
    
    all_files = INIT_FILES + DOC_FILES
    success = 0
    
    for file_spec in all_files:
        if push_file(file_spec["path"], file_spec["content"], file_spec["message"]):
            success += 1
        print()
    
    print("=" * 70)
    print(f"📊 Results: {success}/{len(all_files)} pushed successfully!")
    
    if success == len(all_files):
        print("✅ All documentation files pushed!")

if __name__ == "__main__":
    main()
