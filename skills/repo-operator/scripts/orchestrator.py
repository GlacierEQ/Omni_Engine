#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, subprocess, sys, time
from pathlib import Path

ROOT = Path(".").resolve()
OUT = ROOT / "output"
LOG = OUT / "logs" / "operator.log"

PHASES = [
    ("analysis", "analysis.py"),
    ("completion", "completion.py"),
    ("deployment_prep", "deployment_prep.py"),
    ("validation", "validation.py"),
    ("deploy", "deploy.py"),
]

def log(msg: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "logs").mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"{stamp} | {msg}"
    print(line)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def run(script: str, *, force: bool, apply_patches: bool, dry_run: bool) -> None:
    cmd = [sys.executable, str(ROOT / "scripts" / script)]
    env = os.environ.copy()
    env["OP_FORCE"] = "1" if force else "0"
    env["OP_APPLY_PATCHES"] = "1" if apply_patches else "0"
    env["OP_DRY_RUN"] = "1" if dry_run else "0"
    log(f"RUN {script} force={force} apply_patches={apply_patches} dry_run={dry_run}")
    subprocess.run(cmd, check=True, env=env)

def main() -> None:
    ap = argparse.ArgumentParser(description="Repo Operator 2.1 — hardened orchestrator")
    ap.add_argument("target", nargs="?", default="all",
                    help="phase name (analysis|completion|deployment_prep|validation|deploy) or 'all'")
    ap.add_argument("--force", action="store_true", help="allow overwriting existing files")
    ap.add_argument("--apply-patches", action="store_true", help="apply generated patches to repo")
    ap.add_argument("--dry-run", action="store_true", help="generate reports/patches but do not modify repo")
    args = ap.parse_args()
    
    target = args.target.lower()
    if target == "all":
        for name, script in PHASES:
            run(script, force=args.force, apply_patches=args.apply_patches, dry_run=args.dry_run)
        log("✅ COMPLETE: all phases finished.")
        return

    for name, script in PHASES:
        if target == name:
            run(script, force=args.force, apply_patches=args.apply_patches, dry_run=args.dry_run)
            log(f"✅ COMPLETE: {name}")
            return
    raise SystemExit(f"Unknown target: {target}. Valid: {[n for n,_ in PHASES]} or all")

if __name__ == "__main__":
    main()
