#!/usr/bin/env python3
import subprocess
import os
import json

def test_connection(name, cmd):
    print(f"[📡] Testing {name}...")
    try:
        # Get the absolute path of the directory containing this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Change working directory to the workspace root for the test
        root_dir = os.path.abspath(os.path.join(base_dir, "../../"))
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15, cwd=root_dir)
        if result.returncode == 0:
            print(f"    ✅ {name}: ONLINE")
            return True
        else:
            print(f"    ❌ {name}: FAILED (Code {result.returncode})")
            print(f"       Debug: {result.stderr[:100]}")
            return False
    except Exception as e:
        print(f"    ❌ {name}: ERROR ({str(e)})")
        return False

def run_suite():
    print("🛰️ OMNI_ENGINE CONNECTIVITY VERIFICATION")
    print("---------------------------------------")
    
    results = {}
    results["mcp_cli"] = test_connection("MCP CLI", ["mcp"])
    results["nexus_pattern"] = test_connection("Cognitive Nexus Pattern", ["python3", "omni-engine/core/mission_006_pattern_audit.py"])
    results["mastermind_forensics"] = test_connection("Mastermind Forensics", ["python3", "skills/mastermind/agents/forensic_analyst.py", "."])
    results["mastermind_security"] = test_connection("Mastermind Security", ["python3", "omni-engine/core/mission_004_security.py"])
    results["repo_operator"] = test_connection("Repo Operator Logic", ["python3", "skills/repo-operator/scripts/orchestrator.py"])
    results["universal_factory"] = test_connection("Universal Skill Factory", ["python3", "skills/universal-skill/scripts/factory.py", "TestSkill", "TestDescription"])

    print("\n---------------------------------------")
    summary = "PASSED" if all(results.values()) else "DEGRADED"
    print(f"🏁 INTEGRATION STATUS: {summary}")

if __name__ == "__main__":
    run_suite()
