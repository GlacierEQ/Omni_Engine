# 🌐 UNIVERSAL AI TEAM PROTOCOL (v1.0)
## *The Powerhouse Operating System*

This document defines the standard operating procedure for AI agents working in this environment. It integrates the 50+ core skills with the 69+ MCP servers.

---

### 1. 📂 WORKSPACE ARCHITECTURE
- **/home/user/skills/**: The core intelligence repository.
- **/home/user/skills/cli/**: Orchestration tools (`skills.py`, `skills_enhanced.py`).
- **/home/user/skills/domain-deepdives/**: Strategic knowledge for 9+ domains.
- **/home/user/skills/workflows/**: Step-by-step execution JSONs.

### 2. 🛠️ MCP TOOL MAPPING (PREDICTIONS)
When performing tasks, use these preferred MCP servers:
| Task | Preferred Server | Backup Server |
| :--- | :--- | :--- |
| **Documentation** | `notion` | `google-docs` |
| **Project Tracking** | `linear` (Auth Check Required) | `taskmaster` |
| **Code/Repo** | `github` | `smithery-ai-github` |
| **Search/Research** | `exa` | `perplexity-mcp` |
| **Database** | `supabase-f597` | `mongodb-js-mongodb-mcp-server` |
| **Browser Ops** | `browser-tool` | `browserbase` |

### 3. 🚀 ACTIVATION SEQUENCE
Before starting any major project, run the following:
1. `python3 ~/skills/cli/skills_enhanced.py list` (Identify relevant Power Stack)
2. `python3 ~/skills/cli/skills_enhanced.py deploy [stack]` (Load context)
3. `mcp <server> check_health` (Verify tool availability)

### 4. 🧠 SKILL EXECUTION
AI agents should always check `~/skills/SKILLS_MANIFEST.json` to find the exact skill set required for a task. If a task requires "Data Analysis Pro", refer to `~/skills/domain-deepdives/DATA_ANALYTICS_EXPERT.md` for methodology.

### 5. 🧪 QUALITY ASSURANCE
Every output must be validated against the `success_metrics` defined in the skill templates.

---

**Protocol Active.** Let's build extraordinary things.
