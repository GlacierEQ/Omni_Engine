#!/usr/bin/env python3
import sys
import os
import subprocess

def run_phase(name, script):
    print(f"\n>>> Phase: {name}")
    try:
        subprocess.run([sys.executable, f"scripts/{script}"], check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Error in {name} phase. Aborting.")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Repo Operator 2.0 - Hyper Powerful Build")
        print("Usage: orchestrator [phase|all]")
        sys.exit(0)

    target = sys.argv[1].lower()
    
    phases = [
        ("Analysis", "analysis.py"),
        ("Completion", "completion.py"),
        ("Deployment Prep", "deployment_prep.py"),
        ("Validation", "validation.py"),
        ("Deploy", "deploy.py")
    ]

    if target == "all":
        for name, script in phases:
            run_phase(name, script)
        print("\n🏆 Repository fully finalized and deployed.")
    else:
        # Match target to phase
        found = False
        for name, script in phases:
            if target in name.lower() or target in script.lower():
                run_phase(name, script)
                found = True
                break
        if not found:
            print(f"Unknown target: {target}")

if __name__ == "__main__":
    main()
