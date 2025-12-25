#!/usr/bin/env python3
import os
import json

def deep_audit(directory):
    print(f"[🕵️] Deep Auditor: Inspecting {directory} for hidden architectural debt...")
    findings = {
        "security": [],
        "performance": [],
        "structural": []
    }
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            # Check for large files (Performance)
            if os.path.getsize(path) > 1024 * 1024:
                findings["performance"].append(f"LARGE_FILE: {path}")
            # Check for hardcoded secrets (Security)
            if file.endswith((".env", ".py", ".js")):
                with open(path, "r", errors="ignore") as f:
                    content = f.read()
                    if "password" in content.lower() or "secret" in content.lower():
                        findings["security"].append(f"POSSIBLE_SECRET: {path}")
                        
    return findings

if __name__ == "__main__":
    report = deep_audit(".")
    print(json.dumps(report, indent=2))
