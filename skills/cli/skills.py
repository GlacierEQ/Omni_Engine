#!/usr/bin/env python3
"""
🚀 SKILLS COMMAND-LINE INTERFACE
Master orchestrator for deploying AI skills and workflows
"""

import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Any
import argparse
from datetime import datetime

class SkillsOrchestrator:
    def __init__(self):
        self.skills_dir = Path(__file__).parent.parent
        self.skills_manifest = self.load_manifest()
        self.history = []

    def load_manifest(self) -> Dict:
        """Load skills manifest"""
        manifest_path = self.skills_dir / "SKILLS_MANIFEST.json"
        if manifest_path.exists():
            with open(manifest_path) as f:
                return json.load(f)
        return {}

    def list_skills(self, domain: str = None) -> List[str]:
        """List available skills, optionally filtered by domain.

        Works with the structured SKILLS_MANIFEST.json format:
        {"version": ..., "domains": {domain_key: {"skills": [...]}}
        """
        domains = self.skills_manifest.get("domains", {})

        # Optional filter by domain (supports simple aliases like \"data\" → \"data_analysis\")
        if domain:
            key = domain.strip().lower().replace(' ', '_').replace('-', '_')
            alias_map = {
                'data': 'data_analysis',
                'data_analysis': 'data_analysis',
                'content': 'content_creation',
                'content_creation': 'content_creation',
                'dev': 'development',
                'development': 'development',
                'productivity': 'productivity',
                'strategy': 'strategy',
                'automation': 'automation',
                'integration': 'integration',
                'infra': 'integration',
                'infrastructure': 'integration',
                'support': 'integration',
                'communication': 'communication',
                'comms': 'communication',
                'learning': 'learning',
            }
            dom_key = alias_map.get(key, key)
            domain_obj = domains.get(dom_key)
            if not domain_obj:
                return []
            return [s.get('name', '(unnamed)') for s in domain_obj.get('skills', [])]

        # No domain filter: flatten all skill names across domains
        skills: List[str] = []
        for dom in domains.values():
            for s in dom.get('skills', []):
                name = s.get('name')
                if name and name not in skills:
                    skills.append(name)
        return skills

    def get_skill(self, skill_name: str) -> Dict[str, Any]:
        """Get detailed skill information from SKILLS_MANIFEST.json.

        Matches by case-insensitive name or id/slug.
        """
        domains = self.skills_manifest.get('domains', {})
        target = skill_name.strip().lower()

        for domain_key, domain_obj in domains.items():
            for s in domain_obj.get('skills', []):
                name = str(s.get('name', '')).lower()
                sid = str(s.get('id', '')).lower()
                if target in (name, sid):
                    return {
                        'domain_key': domain_key,
                        'domain': domain_key.replace('_', ' ').title(),
                        'skill': s,
                    }
        return None

    def combine_skills(self, skills: List[str], project: str = None) -> Dict[str, Any]:
        """Combine multiple skills for a project"""
        return {
            "project": project or "Custom Project",
            "skills": skills,
            "timestamp": datetime.now().isoformat(),
            "count": len(skills),
            "combination_id": f"combo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }

    def deploy_workflow(self, workflow: str) -> Dict[str, Any]:
        """Deploy a predefined workflow"""
        workflows_dir = self.skills_dir / "workflows"
        workflow_file = workflows_dir / f"{workflow}.json"
        
        if workflow_file.exists():
            with open(workflow_file) as f:
                return json.load(f)
        return {"error": f"Workflow '{workflow}' not found"}

    def list_templates(self) -> List[str]:
        """List available project templates"""
        templates_dir = self.skills_dir / "templates"
        if templates_dir.exists():
            return [f.stem for f in templates_dir.glob("*.json")]
        return []

    def get_template(self, template: str) -> Dict[str, Any]:
        """Get project template"""
        templates_dir = self.skills_dir / "templates"
        template_file = templates_dir / f"{template}.json"
        
        if template_file.exists():
            with open(template_file) as f:
                return json.load(f)
        return {"error": f"Template '{template}' not found"}

    def save_combination(self, combination: Dict[str, Any]) -> str:
        """Save a skill combination for reuse"""
        combos_dir = self.skills_dir / "combinations"
        combos_dir.mkdir(exist_ok=True)
        
        combo_file = combos_dir / f"{combination['combination_id']}.json"
        with open(combo_file, 'w') as f:
            json.dump(combination, f, indent=2)
        
        return f"Combination saved: {combo_file}"

    def quick_deploy(self, preset: str) -> Dict[str, Any]:
        """Quick deploy with preset combinations"""
        presets = {
            "saas": ["Strategic Planner", "Market Analyst", "Full-Stack Architect", "DevOps Master", "Product Manager", "Sales Strategist"],
            "data": ["Data Analyst Pro", "Database Architect", "ML Engineer", "Data Visualization Expert", "Executive Communicator"],
            "marketing": ["Content Strategist", "Copywriter Elite", "Social Media Maven", "Video Scriptwriter", "SEO Optimizer", "Sales Strategist"],
            "automation": ["Workflow Automator", "System Integrator", "API Orchestrator", "DevOps Master", "Quality Assurance Master"],
            "ai": ["AI Integrator", "Backend Engineer", "Full-Stack Architect", "Security Architect"],
            "product": ["UX Designer Pro", "Frontend Wizard", "Backend Engineer", "DevOps Master", "Product Manager", "Customer Success Manager"],
        }
        
        if preset in presets:
            return self.combine_skills(presets[preset], f"{preset.upper()} Stack")
        return {"error": f"Unknown preset: {preset}"}

def main():
    parser = argparse.ArgumentParser(
        description="🚀 Skills Orchestrator - Deploy AI skills & workflows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  skills list                           # List all skills
  skills list --domain data             # List data skills
  skills get "Data Analyst Pro"         # Get skill details
  skills combine skill1 skill2 skill3   # Combine skills
  skills quick-deploy saas              # Quick deploy SaaS stack
  skills workflow launch-saas            # Deploy workflow
  skills template product-mvp           # Get template
  skills save-combo skill1 skill2       # Save combination
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # List command
    list_parser = subparsers.add_parser('list', help='List available skills')
    list_parser.add_argument('--domain', help='Filter by domain')

    # Get command
    get_parser = subparsers.add_parser('get', help='Get skill details')
    get_parser.add_argument('skill', help='Skill name')

    # Combine command
    combine_parser = subparsers.add_parser('combine', help='Combine multiple skills')
    combine_parser.add_argument('skills', nargs='+', help='Skills to combine')
    combine_parser.add_argument('--project', help='Project name')

    # Quick deploy command
    quick_parser = subparsers.add_parser('quick-deploy', help='Quick deploy preset stacks')
    quick_parser.add_argument('preset', choices=['saas', 'data', 'marketing', 'automation', 'ai', 'product'],
                             help='Preset stack to deploy')

    # Workflow command
    workflow_parser = subparsers.add_parser('workflow', help='Deploy workflow')
    workflow_parser.add_argument('workflow', help='Workflow name')

    # Template command
    template_parser = subparsers.add_parser('template', help='Get project template')
    template_parser.add_argument('template', help='Template name')

    # List templates command
    templates_parser = subparsers.add_parser('templates', help='List available templates')

    # Save combo command
    save_parser = subparsers.add_parser('save-combo', help='Save skill combination')
    save_parser.add_argument('skills', nargs='+', help='Skills to save')

    args = parser.parse_args()
    orchestrator = SkillsOrchestrator()

    if args.command == 'list':
        print("\n🎯 AVAILABLE SKILLS\n")
        skills = orchestrator.list_skills(args.domain)
        for i, skill in enumerate(skills, 1):
            print(f"{i}. {skill}")
        print()

    elif args.command == 'get':
        skill_info = orchestrator.get_skill(args.skill)
        if skill_info:
            print(json.dumps(skill_info, indent=2))
        else:
            print(f"Skill not found: {args.skill}")

    elif args.command == 'combine':
        combo = orchestrator.combine_skills(args.skills, args.project)
        print(json.dumps(combo, indent=2))

    elif args.command == 'quick-deploy':
        result = orchestrator.quick_deploy(args.preset)
        print(json.dumps(result, indent=2))

    elif args.command == 'workflow':
        workflow = orchestrator.deploy_workflow(args.workflow)
        print(json.dumps(workflow, indent=2))

    elif args.command == 'template':
        template = orchestrator.get_template(args.template)
        print(json.dumps(template, indent=2))

    elif args.command == 'templates':
        templates = orchestrator.list_templates()
        print("\n📋 AVAILABLE TEMPLATES\n")
        for i, t in enumerate(templates, 1):
            print(f"{i}. {t}")
        print()

    elif args.command == 'save-combo':
        combo = orchestrator.combine_skills(args.skills)
        message = orchestrator.save_combination(combo)
        print(message)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
