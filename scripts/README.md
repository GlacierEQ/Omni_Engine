# 🔧 Scripts & Utilities

All your utility scripts in one place.

---

## 📋 Available Scripts

### Memory Management
**`memory_manager.py`**
- Purpose: Manage memory systems
- Usage: `python memory_manager.py [options]`
- Docs: See `docs/current/MEMORY_SYSTEM_GUIDE.md`

**`memory_commands.sh`**
- Purpose: Memory CLI commands
- Usage: `bash memory_commands.sh [command]`
- Note: Companion to memory_manager.py

**`memory_demo.sh`**
- Purpose: Demo memory system features
- Usage: `bash memory_demo.sh`
- Note: Educational/demonstration script

**`memory_system_setup.sh`**
- Purpose: Initial memory system setup
- Usage: `bash memory_system_setup.sh`
- Note: Run once during setup

### Document & Skill Pushers
**`push_skills_to_omni.py`**
- Purpose: Push skills to Omni engine
- Usage: `python push_skills_to_omni.py`
- Location: Uses `skills/` directory
- Docs: See `OMNI_ENGINE_SKILLS_PUSH_PACKAGE.md`

**`push_docs_to_omni.py`**
- Purpose: Push documentation to Omni engine
- Usage: `python push_docs_to_omni.py`
- Location: Uses `docs/` directory
- Docs: See `OMNI_ENGINE_INTEGRATION_PLAN.md`

### Setup & Configuration
**`NOTION_SETUP_TEMPLATE.sh`**
- Purpose: Set up Notion integration
- Usage: `bash NOTION_SETUP_TEMPLATE.sh`
- Config: Modify environment variables first
- Docs: See `docs/current/NOTION_CONNECTOR_GUIDE.md`

**`GITHUB_COMMIT_STRATEGY.sh`**
- Purpose: Git workflow and commit strategy
- Usage: `bash GITHUB_COMMIT_STRATEGY.sh [action]`
- Note: Define your Git workflow

### Utilities
**`final_push.py`**
- Purpose: Final deployment push
- Usage: `python final_push.py`
- Note: Use for final deployments

---

## 🚀 Quick Start

### Setup Memory System
```bash
cd scripts/
bash memory_system_setup.sh
```

### Push Skills to Omni
```bash
python push_skills_to_omni.py
```

### Demo Memory Features
```bash
bash memory_demo.sh
```

### Setup Notion Integration
```bash
# First: Edit NOTION_SETUP_TEMPLATE.sh and set your credentials
bash NOTION_SETUP_TEMPLATE.sh
```

---

## 📝 Dependencies

**Python Scripts** require:
- Python 3.7+
- See individual scripts for module requirements

**Shell Scripts** require:
- Bash 4.0+
- Standard Unix utilities (curl, etc.)

---

## ⚙️ Configuration

Most scripts read from environment or `.env` files.

**Setup environment**:
```bash
# Create .env file in scripts/ or use exported variables
export NOTION_API_KEY="your-key"
export PERPLEXITY_API_KEY="your-key"
# etc.
```

---

## 🔗 Related Documentation

- Memory System: `docs/current/MEMORY_SYSTEM_GUIDE.md`
- Notion Integration: `docs/current/NOTION_CONNECTOR_GUIDE.md`
- Omni Engine: `docs/archived/OMNI_ENGINE_INTEGRATION_PLAN.md`
- MCP Setup: `docs/current/MCP_BEST_PRACTICES_AND_DEPLOYMENT_PLAN.md`

---

## 📊 All Scripts

| Script | Type | Purpose |
|--------|------|---------|
| `memory_manager.py` | Python | Memory management |
| `memory_commands.sh` | Shell | Memory CLI |
| `memory_demo.sh` | Shell | Memory demo |
| `memory_system_setup.sh` | Shell | Setup memory |
| `push_skills_to_omni.py` | Python | Push skills |
| `push_docs_to_omni.py` | Python | Push docs |
| `NOTION_SETUP_TEMPLATE.sh` | Shell | Setup Notion |
| `GITHUB_COMMIT_STRATEGY.sh` | Shell | Git workflow |
| `final_push.py` | Python | Final deployment |

---

**Back to**: [`README.md`](../README.md)

**Master Index**: [`INDEX.md`](../INDEX.md)
