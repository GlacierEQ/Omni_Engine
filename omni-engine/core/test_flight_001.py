#!/usr/bin/env python3
import subprocess
import time

def run_mission():
    print("🚀 INITIALIZING TEST FLIGHT 001")
    print("--------------------------------")
    
    # Step 1: Cognitive Nexus Command
    print("[🧠] AI Cognitive Nexus: Directing Mastermind Fleet...")
    time.sleep(1)
    
    # Step 2: Invoke Forensic Analyst
    print("[🔍] Mastermind: Deploying Forensic Analyst Agent...")
    result = subprocess.run(["python3", "skills/mastermind/agents/forensic_analyst.py", "skills/repo-operator"], 
                            capture_output=True, text=True)
    
    print("\n[📊] Analysis Report Received:")
    print(result.stdout)
    
    # Step 3: Log to Mission Control
    print("[🛰️] Mission Control: Updating Dashboard...")
    subprocess.run(["sed", "-i", "s/- \[ \] Recursive scan/- \[x\] Recursive scan/", "dashboard/mission_control.md"])
    
    print("\n✅ MISSION COMPLETE: Repository analyzed and logged.")

if __name__ == "__main__":
    run_mission()
