# Supermemory Integration for the Skills System

This repo is wired to push its entire skills system into Supermemory via MCP.

Key files:
- `skills/SUPERMEMORY_SKILLS_PAYLOADS.json` – prebuilt memory chunks (global, per-domain, local implementation skills)
- `skills/SUPERMEMORY_PROJECT_MAPPING.json` – maps each payload/domain to a Supermemory projectId
- `skills/cli/push_to_supermemory.py` – helper script to call `mcp supermemory addMemory`

## 1. One-time / periodic push into Supermemory

From your shell (not inside a sandbox):

```bash
cd ~/skills

# Preview what will be sent, without changing Supermemory
python3 cli/push_to_supermemory.py --dry-run

# Actually push all payloads
python3 cli/push_to_supermemory.py
```

This will:
- Read all payloads from `SUPERMEMORY_SKILLS_PAYLOADS.json`
- Resolve a `projectId` for each, using `SUPERMEMORY_PROJECT_MAPPING.json`
- Call `mcp supermemory addMemory '{"thingToRemember":..., "projectId":...}'` for each

## 2. Project routing (where memories go)

Current mapping (see `SUPERMEMORY_PROJECT_MAPPING.json`):

- **Default project**: `sm_project_memory_master`  
  Used when nothing more specific is configured.

- **By payload id**:
  - `skills_global_overview` → `sm_project_memory_master`  
    (High-level overview of the entire Power Skills System.)
  - `skills_local_implementation` → `sm_project_computers`  
    (Workspace-local tools like pdf, gemini, file-organizer, forensics/tools, brainstorming.)

- **By domain** (payload ids like `skills_domain_<domain_key>`):
  - `data_analysis` → `sm_project_business`
  - `content_creation` → `sm_project_business`
  - `development` → `sm_project_computers`
  - `productivity` → `sm_project_task_scheduled_ops`
  - `strategy` → `sm_project_business`
  - `automation` → `sm_project_task_scheduled_ops`
  - `communication` → `sm_project_business`
  - `learning` → `sm_project_memory_master`
  - `integration` → `sm_project_computers`

You can edit `SUPERMEMORY_PROJECT_MAPPING.json` to change any of this before running the push script.

## 3. Using Supermemory search with these skills

Once the payloads are stored, you can use `supermemory.search` to pull back the right context.

### 3.1. Ask about the overall skills system

```bash
mcp supermemory search '{
  "informationToGet": "overview of my Power Skills System and domains",
  "projectId": "sm_project_memory_master"
}'
```

### 3.2. Ask about development / coding skills

```bash
mcp supermemory search '{
  "informationToGet": "my development and engineering skills and how to use them",
  "projectId": "sm_project_computers"
}'
```

### 3.3. Ask about automation & operations workflows

```bash
mcp supermemory search '{
  "informationToGet": "automation, workflows, and productivity-related skills",
  "projectId": "sm_project_task_scheduled_ops"
}'
```

### 3.4. Ask about content / business strategy skills

```bash
mcp supermemory search '{
  "informationToGet": "content, marketing, and strategy skills I have defined",
  "projectId": "sm_project_business"
}'
```

### 3.5. Ask about local implementation tools (pdf, gemini, forensics, etc.)

```bash
mcp supermemory search '{
  "informationToGet": "workspace-local tools and skills like pdf processing, Gemini CLI, file organization, and forensics",
  "projectId": "sm_project_computers"
}'
```

## 4. Limiting pushes to specific payloads

To only push a subset (for example, just the global overview):

```bash
cd ~/skills
python3 cli/push_to_supermemory.py --only-id skills_global_overview
```

You can repeat `--only-id` to include multiple payloads.

## 5. Adjusting the integration

- To change routing: edit `SUPERMEMORY_PROJECT_MAPPING.json` and re-run the script.
- To change what’s stored: regenerate or edit `SUPERMEMORY_SKILLS_PAYLOADS.json`, then push again.
