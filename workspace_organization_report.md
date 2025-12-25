# Workspace Organization Analysis & Plan

## Current State Summary
- **Root directory clutter**: 60+ files directly in /home/user/
- **No true duplicates** found (by SHA256 hash)
- **Dominant file types**: Markdown (.md), scripts (.sh), text (.txt)
- **Scattered documentation** across root and subfolders
- **Active projects**: master-toolbox, skills, supabase-pro, mcp-*

## Issues Identified
1. **Root directory chaos** - mixed docs, scripts, symlinks, configs
2. **Documentation sprawl** - MD/TXT files everywhere
3. **Symlink clutter** - tools scattered as root shortcuts  
4. **Inactive folders** - github-mcp, nuclear-output, overleaf-factory

## Proposed Structure
```
/home/user/
├── 📁 active-projects/
│   ├── master-toolbox/
│   ├── supabase-pro/
│   ├── mcp-integration/
│   └── mcp-elevation/
├── 📁 skills/                 [keep as-is]
├── 📁 docs/
│   ├── analysis/
│   ├── deployment/
│   └── reference/
├── 📁 scripts/
├── 📁 tools/                  [consolidate symlinks]
├── 📁 archive/                [inactive projects]
└── README.md
```

## Action Plan (Safe - No Overwrites)
```
1. mkdir -p /home/user/{active-projects,docs/{analysis,deployment,reference},scripts,tools,archive}
2. Move MD/TXT files → docs/analysis/
3. Move .sh files → scripts/
4. Consolidate symlinks → tools/
5. Move inactive folders → archive/
```

## Commands Ready to Run
```bash
# Preview moves (dry run)
find /home/user -maxdepth 1 -name "*.md" -o -name "*.txt"

# Execute organization (safe)
./organize_workspace.sh  # [Will create this script]
```

**Approve to proceed with cleanup? (y/n)**

"

## ✅ Ready to Execute
Run: `bash organize_workspace.sh` for dry-run preview
Run: `bash organize_workspace.sh --execute` to organize."
