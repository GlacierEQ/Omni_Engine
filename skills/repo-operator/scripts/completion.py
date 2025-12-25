from __future__ import annotations
import os, json, difflib
from pathlib import Path

ROOT = Path(".").resolve()
OUT = ROOT / "output"
PATCHES = ROOT / "patches"
OUT.mkdir(parents=True, exist_ok=True)
PATCHES.mkdir(parents=True, exist_ok=True)

FORCE = os.getenv("OP_FORCE", "0") == "1"
APPLY = os.getenv("OP_APPLY_PATCHES", "0") == "1"
DRY = os.getenv("OP_DRY_RUN", "0") == "1"

def write_patch(path: Path, new_content: str) -> Path:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    diff = difflib.unified_diff(
        old.splitlines(True),
        new_content.splitlines(True),
        fromfile=str(path),
        tofile=str(path),
    )
    patch_text = "".join(diff)
    patch_path = PATCHES / (path.name + ".diff")
    patch_path.write_text(patch_text, encoding="utf-8")
    return patch_path

def maybe_apply(path: Path, content: str) -> None:
    if DRY:
        return
    if path.exists() and not FORCE:
        # no overwrite unless force
        return
    path.write_text(content, encoding="utf-8")

def main():
    repo_map_path = OUT / "repo_map.json"
    if not repo_map_path.exists():
        print("⚠️ No output/repo_map.json; run analysis first.")
        return
    m = json.loads(repo_map_path.read_text(encoding="utf-8"))
    missing = m.get("missing_elements", [])
    
    # README
    if "README.md" in missing:
        content = "# Repository\n\nAuto-generated baseline README.\n"
        p = ROOT / "README.md"
        patch = write_patch(p, content)
        maybe_apply(p, content)
        print(f"🧩 README patch -> {patch}")
        
    # .env.example
    if ".env.example" in missing:
        content = "PORT=3000\n# Add env vars here (never commit real secrets)\n"
        p = ROOT / ".env.example"
        patch = write_patch(p, content)
        maybe_apply(p, content)
        print(f"🧩 .env.example patch -> {patch}")
        
    # .gitignore (baseline safety)
    if ".gitignore" in missing:
        content = "\n".join([
            ".venv/",
            "__pycache__/",
            "node_modules/",
            ".env",
            ".env.*",
            "output/",
            "*.log",
            "dist/",
            "build/",
        ]) + "\n"
        p = ROOT / ".gitignore"
        patch = write_patch(p, content)
        maybe_apply(p, content)
        print(f"🧩 .gitignore patch -> {patch}")
    print("✅ Completion complete (patches generated; apply depends on flags).")

if __name__ == "__main__":
    main()
