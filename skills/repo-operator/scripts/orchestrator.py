#!/usr/bin/env python3
import json
import os
import sys

def main():
    print("Repo Operator Protocol 2.0 - Orchestrator")
    print("=========================================")
    
    # Load manifest
    manifest_path = os.path.join(os.path.dirname(__file__), '..', 'protocol_manifest.json')
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
        
    print(f"Version: {manifest['version']}")
    print(f"Intent: {manifest['meta']['intent']}")
    print("\nPhases:")
    for phase in manifest['phases']:
        print(f"- {phase['name']}: {', '.join(phase['tasks'])}")
    
    print("\nOrchestrator ready. Use individual phase scripts or call with phase name.")

if __name__ == "__main__":
    main()
