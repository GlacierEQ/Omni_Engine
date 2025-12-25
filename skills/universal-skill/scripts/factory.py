#!/usr/bin/env python3
import os
import json
import sys

def create_skill(name, description, domain="general"):
    skill_id = name.lower().replace(" ", "-")
    path = f"skills/{skill_id}"
    os.makedirs(f"{path}/scripts", exist_ok=True)
    
    # Create SKILL.md
    with open(f"{path}/SKILL.md", "w") as f:
        f.write(f"# {name}\n\n{description}\n")
        
    # Update Manifest
    manifest_path = "skills/SKILLS_MANIFEST.json"
    if os.path.exists(manifest_path):
        with open(manifest_path, "r") as f:
            data = json.load(f)
        
        if domain not in data["domains"]:
            data["domains"][domain] = {"skills": []}
            
        data["domains"][domain]["skills"].append({
            "id": skill_id,
            "name": name,
            "description": description
        })
        data["total_skills"] += 1
        
        with open(manifest_path, "w") as f:
            json.dump(data, f, indent=2)
            
    return f"Skill {name} created at {path}"

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(create_skill(sys.argv[1], sys.argv[2]))
