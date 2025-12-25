#!/usr/bin/env python3
"""
Skills Orchestrator - Master command interface for the skills system
Integrates all modules: skills, workflows, powerups, forensics
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class SkillsOrchestrator:
    def __init__(self):
        self.base_path = Path("/home/user/skills")
        self.skills_file = self.base_path / "SKILLS_50_COMPLETE.json"
        self.powerups_file = self.base_path / "powerups" / "POWERUPS_EXTENDED.json"
        self.forensics_file = self.base_path / "forensics" / "FORENSIC_SCHEMA_EXTENDED.json"
        self.workflows_dir = self.base_path / "workflows"
        self.templates_dir = self.base_path / "templates"
        self.load_all()

    def load_all(self):
        """Load all system components"""
        try:
            with open(self.skills_file) as f:
                self.skills = json.load(f)
            print(f"✅ Loaded {len(self.skills.get('skills', []))} skills")
        except Exception as e:
            print(f"❌ Error loading skills: {e}")
            self.skills = {}

        try:
            with open(self.powerups_file) as f:
                self.powerups = json.load(f)
            print(f"✅ Loaded {self.powerups.get('meta', {}).get('total_powerups', 0)} powerups")
        except Exception as e:
            print(f"⚠️  Powerups file not found: {e}")
            self.powerups = {}

        try:
            with open(self.forensics_file) as f:
                self.forensics = json.load(f)
            print(f"✅ Loaded forensics schema with {len(self.forensics.get('forensic_categories', []))} categories")
        except Exception as e:
            print(f"⚠️  Forensics file not found: {e}")
            self.forensics = {}

    def list_skills_by_category(self) -> Dict[str, List]:
        """Group skills by category"""
        categories = {}
        for skill in self.skills.get('skills', []):
            cat = skill.get('category', 'Uncategorized')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(skill)
        return categories

    def search_skills(self, query: str) -> List:
        """Search skills by name or description"""
        query = query.lower()
        results = []
        for skill in self.skills.get('skills', []):
            if (query in skill.get('name', '').lower() or 
                query in skill.get('description', '').lower()):
                results.append(skill)
        return results

    def get_skill_details(self, skill_id: int) -> Optional[Dict]:
        """Get detailed info for a specific skill"""
        for skill in self.skills.get('skills', []):
            if skill.get('id') == skill_id:
                return skill
        return None

    def get_powerups_for_skill(self, skill_id: int) -> List:
        """Get applicable powerups for a skill"""
        skill = self.get_skill_details(skill_id)
        if not skill:
            return []
        
        applicable = []
        for category in self.powerups.get('powerup_categories', []):
            for powerup in category.get('powerups', []):
                # Match based on category or description
                if skill.get('category') in powerup.get('description', '').lower():
                    applicable.append(powerup)
        return applicable

    def get_forensic_report(self, skill_id: int) -> Dict:
        """Generate forensic report template for skill"""
        skill = self.get_skill_details(skill_id)
        if not skill:
            return {}
        
        report = {
            "skill_id": skill_id,
            "skill_name": skill.get('name'),
            "generated_at": datetime.now().isoformat(),
            "sections": {}
        }
        
        for category in self.forensics.get('forensic_categories', []):
            report['sections'][category['name']] = {
                "description": category['description'],
                "metrics": [m['name'] for m in category.get('metrics', [])]
            }
        
        return report

    def create_skill_execution_plan(self, skill_id: int) -> Dict:
        """Create execution plan: skill + powerups + forensics"""
        skill = self.get_skill_details(skill_id)
        if not skill:
            return {"error": "Skill not found"}
        
        powerups = self.get_powerups_for_skill(skill_id)
        forensics = self.get_forensic_report(skill_id)
        
        plan = {
            "execution_plan": {
                "timestamp": datetime.now().isoformat(),
                "skill": {
                    "id": skill.get('id'),
                    "name": skill.get('name'),
                    "category": skill.get('category'),
                    "level": skill.get('level'),
                    "capabilities": skill.get('capabilities', [])
                },
                "recommended_powerups": [
                    {
                        "name": p.get('name'),
                        "boost": p.get('boost'),
                        "implementation_time": p.get('time_to_implement')
                    }
                    for p in powerups[:3]  # Top 3 powerups
                ],
                "forensic_tracking": {
                    "key_metrics": list(forensics.get('sections', {}).keys()),
                    "report_frequency": "Weekly, Monthly, Quarterly"
                },
                "success_criteria": {
                    "adoption_target": "> 60% team adoption",
                    "quality_target": "> 90% quality score",
                    "roi_target": "Positive ROI within 6 months"
                }
            }
        }
        return plan

    def display_system_status(self) -> str:
        """Show overall system health and stats"""
        categories = self.list_skills_by_category()
        stats = {
            "total_skills": len(self.skills.get('skills', [])),
            "categories": len(categories),
            "powerups": self.powerups.get('meta', {}).get('total_powerups', 0),
            "forensic_categories": len(self.forensics.get('forensic_categories', [])),
            "skills_per_category": {cat: len(skills) for cat, skills in categories.items()}
        }
        return json.dumps(stats, indent=2)

    def export_skill_to_markdown(self, skill_id: int) -> str:
        """Export skill details as markdown"""
        skill = self.get_skill_details(skill_id)
        if not skill:
            return "# Skill not found"
        
        md = f"""# {skill.get('name')}

**Category:** {skill.get('category')}  
**Level:** {skill.get('level')}  
**ID:** {skill.get('id')}

## Description
{skill.get('description')}

## Capabilities
{', '.join(skill.get('capabilities', []))}

## Technologies
{', '.join(skill.get('technologies', []))}

## Use Cases
{', '.join(skill.get('use_cases', []))}
"""
        return md

    def run_command(self, command: str, args: List[str]) -> str:
        """Execute orchestrator commands"""
        commands = {
            "list": lambda: self._cmd_list(),
            "search": lambda: self._cmd_search(args[0] if args else ""),
            "details": lambda: self._cmd_details(int(args[0]) if args else 0),
            "plan": lambda: self._cmd_plan(int(args[0]) if args else 0),
            "status": lambda: self.display_system_status(),
            "export": lambda: self._cmd_export(int(args[0]) if args else 0),
            "powerups": lambda: self._cmd_powerups(int(args[0]) if args else 0),
        }
        
        if command in commands:
            return commands[command]()
        return f"Unknown command: {command}"

    def _cmd_list(self) -> str:
        categories = self.list_skills_by_category()
        output = "📚 Skills by Category:\n\n"
        for cat, skills in sorted(categories.items()):
            output += f"**{cat}** ({len(skills)} skills)\n"
            for skill in skills:
                output += f"  - {skill['name']} (Level: {skill['level']})\n"
        return output

    def _cmd_search(self, query: str) -> str:
        if not query:
            return "Please provide a search query"
        results = self.search_skills(query)
        output = f"🔍 Search results for '{query}':\n\n"
        for skill in results:
            output += f"**{skill['name']}** (ID: {skill['id']})\n"
            output += f"  Category: {skill['category']}\n"
            output += f"  Description: {skill['description']}\n\n"
        return output if results else "No skills found"

    def _cmd_details(self, skill_id: int) -> str:
        skill = self.get_skill_details(skill_id)
        if not skill:
            return f"Skill {skill_id} not found"
        return json.dumps(skill, indent=2)

    def _cmd_plan(self, skill_id: int) -> str:
        plan = self.create_skill_execution_plan(skill_id)
        return json.dumps(plan, indent=2)

    def _cmd_export(self, skill_id: int) -> str:
        return self.export_skill_to_markdown(skill_id)

    def _cmd_powerups(self, skill_id: int) -> str:
        powerups = self.get_powerups_for_skill(skill_id)
        output = f"⚡ Powerups for Skill {skill_id}:\n\n"
        for pu in powerups[:5]:
            output += f"**{pu['name']}**\n"
            output += f"  Boost: {pu['boost']}\n"
            output += f"  Time: {pu['time_to_implement']}\n\n"
        return output if powerups else "No applicable powerups found"


def main():
    orchestrator = SkillsOrchestrator()
    
    if len(sys.argv) < 2:
        print("""
🎯 Skills Orchestrator - Usage:
  python skills_orchestrator.py list              # List all skills
  python skills_orchestrator.py search <query>    # Search skills
  python skills_orchestrator.py details <id>      # Get skill details
  python skills_orchestrator.py plan <id>         # Create execution plan
  python skills_orchestrator.py status            # System status
  python skills_orchestrator.py export <id>       # Export as markdown
  python skills_orchestrator.py powerups <id>     # Get powerups for skill
        """)
        print(orchestrator.display_system_status())
        return
    
    command = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    result = orchestrator.run_command(command, args)
    print(result)


if __name__ == "__main__":
    main()
