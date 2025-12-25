from __future__ import annotations
import os, json, time, hashlib
from pathlib import Path
from collections import Counter

ROOT = Path(".").resolve()
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)
IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "dist", "build", ".next", ".cache"}
SIGNALS = {
    "package.json": "node",
    "pnpm-lock.yaml": "node",
    "yarn.lock": "node",
    "requirements.txt": "python",
    "pyproject.toml": "python",
    "Pipfile": "python",
    "Dockerfile": "docker",
    "docker-compose.yml": "docker",
    ".github/workflows": "ci",
    "README.md": "docs",
}
REQUIRED = ["README.md", ".env.example", ".gitignore"]

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def scan():
    tech = set()
    files = 0
    ext_counter = Counter()
    largest = []
    for root, dirs, fs in os.walk(ROOT):
        r = Path(root)
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in fs:
            p = r / f
            if p.is_symlink():
                continue
            files += 1
            ext_counter[p.suffix.lower() or "<none>"] += 1
            # tech signals
            rel = p.relative_to(ROOT)
            if rel.name in SIGNALS:
                tech.add(SIGNALS[rel.name])
            if str(rel).startswith(".github/workflows"):
                tech.add("ci")
            # largest files quick list
            try:
                sz = p.stat().st_size
                largest.append((sz, str(rel)))
            except Exception:
                pass
    # missing required
    missing = []
    for req in REQUIRED:
        if not (ROOT / req).exists():
            missing.append(req)
    largest.sort(reverse=True)
    largest = largest[:15]
    report = {
        "meta": {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "root": str(ROOT)},
        "metrics": {"total_files": files},
        "tech_stack": sorted(list(tech)) or ["unknown"],
        "extensions_top": ext_counter.most_common(20),
        "largest_files": largest,
        "missing_elements": missing,
        "flags": {
            "has_env_file": (ROOT / ".env").exists(),
            "has_secrets_risk": any((ROOT / n).exists() for n in [".env", ".env.local", ".env.production"]),
        },
    }
    (OUT / "repo_map.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("✅ Analysis complete -> output/repo_map.json")

if __name__ == "__main__":
    scan()
