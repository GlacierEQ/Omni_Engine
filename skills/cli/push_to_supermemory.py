#!/usr/bin/env python3
"""Push the workspace skills system into Supermemory via MCP.

Requires:
  - `mcp` CLI installed and configured with a `supermemory` server
  - `skills/SUPERMEMORY_SKILLS_PAYLOADS.json` (pre-built payloads)
  - Optional: `skills/SUPERMEMORY_PROJECT_MAPPING.json` to control routing

Typical usage (from repo root or ~/skills):

  cd ~/skills
  python3 cli/push_to_supermemory.py --dry-run
  python3 cli/push_to_supermemory.py

You can also limit to specific payload ids:

  python3 cli/push_to_supermemory.py --only-id skills_global_overview
"""

import argparse
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List

ROOT = Path(__file__).resolve().parent.parent
PAYLOAD_FILE = ROOT / "SUPERMEMORY_SKILLS_PAYLOADS.json"
MAPPING_FILE = ROOT / "SUPERMEMORY_PROJECT_MAPPING.json"

# Fallback mapping if the JSON mapping file is missing
FALLBACK_MAPPING: Dict[str, Any] = {
    "default_project": "sm_project_memory_master",
    "by_payload_id": {
        "skills_global_overview": "sm_project_memory_master",
        "skills_local_implementation": "sm_project_computers",
    },
    "by_domain": {
        "data_analysis": "sm_project_business",
        "content_creation": "sm_project_business",
        "development": "sm_project_computers",
        "productivity": "sm_project_task_scheduled_ops",
        "strategy": "sm_project_business",
        "automation": "sm_project_task_scheduled_ops",
        "communication": "sm_project_business",
        "learning": "sm_project_memory_master",
        "integration": "sm_project_computers",
    },
}


def load_mapping() -> Dict[str, Any]:
    if MAPPING_FILE.exists():
        try:
            return json.loads(MAPPING_FILE.read_text())
        except Exception:
            return FALLBACK_MAPPING
    return FALLBACK_MAPPING


def resolve_project_id(item: Dict[str, Any], mapping: Dict[str, Any]) -> str:
    """Decide which Supermemory projectId to use for a given payload item."""
    default_project = mapping.get("default_project", "sm_project_memory_master")
    by_id = mapping.get("by_payload_id", {})
    by_domain = mapping.get("by_domain", {})

    pid = None
    payload_id = item.get("id")
    domain = item.get("domain")

    if payload_id and payload_id in by_id:
        pid = by_id[payload_id]
    elif domain and domain in by_domain:
        pid = by_domain[domain]
    else:
        pid = default_project

    return pid


def call_supermemory_add(thing: str, project_id: str, dry_run: bool) -> None:
    args = {"thingToRemember": thing}
    if project_id:
        args["projectId"] = project_id

    args_json = json.dumps(args)

    if dry_run:
        print(f"[DRY RUN] mcp supermemory addMemory '{args_json}'")
        return

    cmd: List[str] = ["mcp", "supermemory", "addMemory", args_json]
    res = subprocess.run(cmd, capture_output=True, text=True)

    print("  exitCode:", res.returncode)
    if res.stdout.strip():
        print("  stdout:", res.stdout.strip())
    if res.stderr.strip():
        print("  stderr:", res.stderr.strip())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Push skills payloads into Supermemory via MCP",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the mcp calls without executing them",
    )
    parser.add_argument(
        "--only-id",
        action="append",
        help="Limit to specific payload id(s) (can be repeated)",
    )

    args = parser.parse_args()

    if not PAYLOAD_FILE.exists():
        raise SystemExit(f"Payload file not found: {PAYLOAD_FILE}")

    data = json.loads(PAYLOAD_FILE.read_text())
    payloads: List[Dict[str, Any]] = data.get("payloads", [])

    mapping = load_mapping()

    print(f"Found {len(payloads)} payloads in {PAYLOAD_FILE}")

    for item in payloads:
        pid = item.get("id")
        if args.only_id and pid not in args.only_id:
            continue

        thing = (item.get("thingToRemember") or "").strip()
        if not thing:
            continue

        project_id = resolve_project_id(item, mapping)
        print(f"\n=== supermemory.addMemory id={pid} -> projectId={project_id}")
        call_supermemory_add(thing, project_id, args.dry_run)


if __name__ == "__main__":
    main()
