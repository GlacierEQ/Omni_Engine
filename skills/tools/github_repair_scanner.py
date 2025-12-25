#!/usr/bin/env python3
"""GitHub Repair Repo Scanner - Compiles tech repair libraries"""

import json
import sys
from datetime import datetime
from typing import Dict, List, Optional

class RepairRepoScanner:
    def __init__(self):
        self.repos = []
        self.categories = {}
    
    def add_repo(self, name: str, url: str, category: str,
                 description: str, tags: List[str],
                 subcategory: Optional[str] = None):
        repo = {
            "name": name, "url": url, "category": category,
            "subcategory": subcategory or "General",
            "description": description, "tags": tags,
            "added_date": datetime.now().isoformat()
        }
        self.repos.append(repo)
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(name)
        return repo
    
    def get_repos_by_category(self, category: str):
        return [r for r in self.repos if r['category'] == category]
    
    def get_repos_by_tag(self, tag: str):
        return [r for r in self.repos if tag in r['tags']]
    
    def export_json(self):
        return json.dumps({
            "title": "Tech Repair & Analysis Library",
            "generated": datetime.now().isoformat(),
            "total_repos": len(self.repos),
            "categories": len(self.categories),
            "repos": self.repos
        }, indent=2)
    
    def export_markdown(self):
        md = "# 🔧 Tech Repair & Analysis Library\n\n"
        md += f"**Total:** {len(self.repos)} repos | **Categories:** {len(self.categories)}\n\n"
        for cat in sorted(self.categories.keys()):
            repos = self.get_repos_by_category(cat)
            md += f"## {cat} ({len(repos)})\n\n"
            for repo in repos:
                md += f"### [{repo['name']}]({repo['url']})\n"
                md += f"- {repo['description']}\n"
                md += f"- **Tags:** {', '.join(repo['tags'])}\n\n"
        return md

def build_scanner():
    scanner = RepairRepoScanner()
    
    repos_data = [
        # OPRYXX CORE
        ("OPRYXX-Main", "https://github.com/Opryxx/OPRYXX", "PC & Device Repair", "Main OPRYXX platform", ["repair","diagnostics","pc-hardware","framework"]),
        ("OPRYXX-Diagnostics", "https://github.com/Opryxx/OPRYXX-Diagnostics", "PC & Device Repair", "Advanced diagnostic tools", ["diagnostics","hardware-analysis","testing"]),
        ("OPRYXX-Hardware-Database", "https://github.com/Opryxx/OPRYXX-Hardware-Database", "Reference & Documentation", "Hardware specification database", ["hardware","database","specs"]),
        
        # DIAGNOSTICS
        ("Hardware-Monitor-Suite", "https://github.com/Opryxx/Hardware-Monitor-Suite", "Monitoring & Analysis", "Real-time hardware monitoring", ["monitoring","hardware-health","temperatures"]),
        ("System-Analyzer", "https://github.com/Opryxx/System-Analyzer", "Monitoring & Analysis", "Deep system analysis tool", ["system-analysis","diagnostics","performance"]),
        ("Network-Diagnostics-Tool", "https://github.com/Opryxx/Network-Diagnostics-Tool", "Network & Connectivity", "Network troubleshooting toolkit", ["network","connectivity","diagnostics"]),
        
        # RECOVERY
        ("Data-Recovery-Framework", "https://github.com/Opryxx/Data-Recovery-Framework", "Data Recovery & Backup", "Data recovery from storage devices", ["data-recovery","storage","forensics"]),
        ("Partition-Recovery-Tool", "https://github.com/Opryxx/Partition-Recovery-Tool", "Data Recovery & Backup", "Partition recovery and repair", ["partitions","recovery","disk-management"]),
        
        # OS REPAIR
        ("Windows-Repair-Suite", "https://github.com/Opryxx/Windows-Repair-Suite", "OS Repair & Maintenance", "Windows repair and maintenance", ["windows","repair","maintenance"]),
        ("Linux-System-Repair", "https://github.com/Opryxx/Linux-System-Repair", "OS Repair & Maintenance", "Linux repair and optimization", ["linux","repair","system-admin"]),
        
        # SECURITY
        ("Malware-Scanner-Engine", "https://github.com/Opryxx/Malware-Scanner-Engine", "Security & Malware", "Malware detection and removal", ["security","malware","antivirus"]),
        ("Security-Audit-Tool", "https://github.com/Opryxx/Security-Audit-Tool", "Security & Malware", "Security auditing and scanning", ["security","audit","vulnerabilities"]),
        ("Rootkit-Detection-Suite", "https://github.com/Opryxx/Rootkit-Detection-Suite", "Security & Malware", "Rootkit and threat detection", ["security","rootkit","forensics"]),
        
        # OPTIMIZATION
        ("Performance-Optimizer", "https://github.com/Opryxx/Performance-Optimizer", "Optimization & Tuning", "System performance optimization", ["optimization","performance","tuning"]),
        ("Disk-Cleanup-Manager", "https://github.com/Opryxx/Disk-Cleanup-Manager", "Optimization & Tuning", "Disk cleanup and optimization", ["disk-cleanup","storage","optimization"]),
        ("Memory-Manager", "https://github.com/Opryxx/Memory-Manager", "Optimization & Tuning", "RAM optimization and leak detection", ["memory","ram","optimization"]),
        
        # HARDWARE TESTING
        ("GPU-Stress-Test", "https://github.com/Opryxx/GPU-Stress-Test", "Hardware Testing", "GPU stress testing", ["gpu","testing","stability"]),
        ("CPU-Diagnostic-Suite", "https://github.com/Opryxx/CPU-Diagnostic-Suite", "Hardware Testing", "CPU diagnostics", ["cpu","testing","diagnostics"]),
        ("Storage-Test-Framework", "https://github.com/Opryxx/Storage-Test-Framework", "Hardware Testing", "Storage device testing", ["storage","ssd","hdd","testing"]),
        ("RAM-Diagnostic-Tool", "https://github.com/Opryxx/RAM-Diagnostic-Tool", "Hardware Testing", "RAM memory testing", ["memory","ram","testing"]),
        
        # FIRMWARE
        ("BIOS-Update-Manager", "https://github.com/Opryxx/BIOS-Update-Manager", "Firmware & BIOS", "BIOS update management", ["bios","firmware","updates"]),
        ("Firmware-Recovery-Tool", "https://github.com/Opryxx/Firmware-Recovery-Tool", "Firmware & BIOS", "Firmware recovery", ["firmware","recovery","restoration"]),
        
        # MOBILE
        ("Mobile-Device-Analyzer", "https://github.com/Opryxx/Mobile-Device-Analyzer", "Mobile Device Repair", "Mobile diagnostics", ["mobile","android","ios"]),
        ("Phone-Battery-Analyzer", "https://github.com/Opryxx/Phone-Battery-Analyzer", "Mobile Device Repair", "Battery health analysis", ["battery","health","mobile"]),
        
        # DOCS
        ("Repair-Manuals-Database", "https://github.com/Opryxx/Repair-Manuals-Database", "Documentation & Reference", "Repair manuals", ["manuals","guides","repair-procedures"]),
        ("Troubleshooting-Guide", "https://github.com/Opryxx/Troubleshooting-Guide", "Documentation & Reference", "Troubleshooting procedures", ["troubleshooting","guides","solutions"]),
        
        # UTILITIES
        ("Repair-Toolkit-Utilities", "https://github.com/Opryxx/Repair-Toolkit-Utilities", "Utilities & Helpers", "General-purpose utilities", ["utilities","helpers","tools"]),
        ("Logging-Monitoring-System", "https://github.com/Opryxx/Logging-Monitoring-System", "Utilities & Helpers", "System logging and monitoring", ["logging","monitoring","events"]),
    ]
    
    for name, url, category, desc, tags in repos_data:
        scanner.add_repo(name, url, category, desc, tags)
    
    return scanner

def main():
    scanner = build_scanner()
    
    if len(sys.argv) < 2:
        print(f"✅ Loaded {len(scanner.repos)} repositories in {len(scanner.categories)} categories\n")
        print("Usage:")
        print("  list                  # List all repos")
        print("  category CATEGORY     # Repos in category")
        print("  tag TAG              # Repos with tag")
        print("  json                 # Export as JSON")
        print("  markdown             # Export as markdown\n")
        print("Categories:")
        for cat in sorted(scanner.categories.keys()):
            print(f"  • {cat} ({len(scanner.categories[cat])})")
        return
    
    cmd = sys.argv[1]
    if cmd == "list":
        for i, r in enumerate(scanner.repos, 1):
            print(f"{i:2d}. {r['name']:40s} | {r['category']}")
    elif cmd == "category" and len(sys.argv) > 2:
        repos = scanner.get_repos_by_category(sys.argv[2])
        for r in repos:
            print(f"  • {r['name']}\n    {r['description']}")
    elif cmd == "tag" and len(sys.argv) > 2:
        repos = scanner.get_repos_by_tag(sys.argv[2])
        for r in repos:
            print(f"  • {r['name']}")
    elif cmd == "json":
        print(scanner.export_json())
    elif cmd == "markdown":
        print(scanner.export_markdown())

if __name__ == "__main__":
    main()
