#!/usr/bin/env python3
"""Omni_Engine Skills Module Integration"""

import json
from typing import Dict, List, Optional
from pathlib import Path

class SkillsEngine:
    """Skills engine for Omni_Engine"""
    
    def __init__(self, data_path: Optional[str] = None):
        if data_path is None:
            data_path = Path(__file__).parent.parent / "data"
        self.data_path = Path(data_path)
        self.skills = {}
        self.powerups = {}
        self.forensics = {}
        self.load_all_data()
    
    def load_all_data(self):
        """Load all skills data"""
        try:
            skills_file = self.data_path / "SKILLS_50_COMPLETE.json"
            if skills_file.exists():
                with open(skills_file) as f:
                    self.skills = json.load(f)
            powerups_file = self.data_path / "POWERUPS_EXTENDED.json"
            if powerups_file.exists():
                with open(powerups_file) as f:
                    self.powerups = json.load(f)
            forensics_file = self.data_path / "FORENSIC_SCHEMA_EXTENDED.json"
            if forensics_file.exists():
                with open(forensics_file) as f:
                    self.forensics = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load data: {e}")
    
    def get_skill(self, skill_id: int) -> Optional[Dict]:
        """Get skill by ID"""
        if isinstance(self.skills, dict) and 'skills' in self.skills:
            for skill in self.skills['skills']:
                if skill.get('id') == skill_id:
                    return skill
        return None
    
    def search_skills(self, query: str) -> List[Dict]:
        """Search skills"""
        query = query.lower()
        results = []
        if isinstance(self.skills, dict) and 'skills' in self.skills:
            for skill in self.skills['skills']:
                if (query in skill.get('name', '').lower() or 
                    query in skill.get('description', '').lower()):
                    results.append(skill)
        return results
    
    def get_system_stats(self) -> Dict:
        """Get system stats"""
        skills_count = len(self.skills.get('skills', [])) if isinstance(self.skills, dict) else 0
        powerups_count = sum(
            len(cat.get('powerups', [])) 
            for cat in self.powerups.get('powerup_categories', [])
        ) if isinstance(self.powerups, dict) else 0
        return {
            "total_skills": skills_count,
            "total_powerups": powerups_count,
            "forensic_systems": len(self.forensics.get('forensic_categories', [])) if isinstance(self.forensics, dict) else 0
        }


class SkillsIntegration:
    """Integration handler"""
    
    def __init__(self):
        self.engine = SkillsEngine()
    
    def analyze_for_goal(self, goal: str) -> Dict:
        """Analyze skills for goal"""
        matching_skills = self.engine.search_skills(goal)
        return {
            "goal": goal,
            "matching_skills": matching_skills[:5],
            "total_matches": len(matching_skills)
        }


def integrate_with_omni():
    """Initialize integration"""
    return SkillsIntegration()


if __name__ == "__main__":
    integration = integrate_with_omni()
    print(f"✅ Skills Engine initialized")
    print(f"📊 Stats: {integration.engine.get_system_stats()}")
