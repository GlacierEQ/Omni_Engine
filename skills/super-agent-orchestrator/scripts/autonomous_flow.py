#!/usr/bin/env python3
import subprocess
import os
import json

def run_autonomous_loop(target_repo):
    print(f"🚀 [SUPER-AGENT] Starting Autonomous Flow for: {target_repo}")
    
    # Step 1: Forensics (Mastermind)
    print("[🔍] Phase 1: Mastermind Forensics Audit...")
    audit = subprocess.run(["python3", "skills/mastermind/agents/forensic_analyst.py", target_repo], 
                           capture_output=True, text=True)
    print(audit.stdout)
    
    # Step 2: Analysis & Completion (Repo Operator)
    print("[🛠️] Phase 2: Repo Operator Completion...")
    # Simulate completion based on audit
    subprocess.run(["python3", "mission_002_completion.py"]) 
    
    # Step 3: Security Validation (Mastermind Security)
    print("[🛡️] Phase 3: Security & Compliance Check...")
    subprocess.run(["python3", "mission_004_security.py"])
    
    # Step 4: Notification (Apple Bridge)
    print("[🍎] Phase 4: Mission Success Notification...")
    subprocess.run(["./mission_003_notify.sh", f"Super-Agent completed flow for {target_repo}"])

    print("✅ [SUPER-AGENT] Autonomous Loop Finished.")

if __name__ == "__main__":
    run_autonomous_loop("skills/repo-operator")
