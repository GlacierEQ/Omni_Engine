#!/usr/bin/env python3
import os
import sys
import json

def analyze_repo(repo_path):
    print(f"[🔍] Forensic Analyst: Scanning {repo_path}")
    results = {
        "structure": [],
        "missing_files": [],
        "risk_level": "Low"
    }
    
    critical_files = ["README.md", "LICENSE", "pyproject.toml", ".env.example"]
    
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            results["structure"].append(os.path.join(root, file))
            
    for crit in critical_files:
        if not any(crit in f for f in results["structure"]):
            results["missing_files"].append(crit)
            
    return results

if __name__ == "__main__":
    if len(sys.argv) > 1:
        report = analyze_repo(sys.argv[1])
        print(json.dumps(report, indent=2))
