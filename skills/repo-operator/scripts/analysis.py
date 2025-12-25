import os
import json
import datetime
import re

class RepoAnalyzer:
    def __init__(self, root_dir="."):
        self.root_dir = root_dir
        self.repo_map = {
            "meta": {
                "timestamp": str(datetime.datetime.now()),
                "root": os.path.abspath(root_dir)
            },
            "structure": {},
            "tech_stack": [],
            "dependencies": {},
            "missing_elements": [],
            "metrics": {"total_files": 0, "total_lines": 0}
        }

    def scan(self):
        config_signatures = {
            "package.json": "Node.js",
            "requirements.txt": "Python",
            "pyproject.toml": "Python (Poetry/Pip)",
            "go.mod": "Go",
            "Cargo.toml": "Rust",
            "Dockerfile": "Docker",
            "Makefile": "Build Tool",
            ".gitignore": "Git",
            "README.md": "Documentation",
            "LICENSE": "Legal"
        }

        for root, dirs, files in os.walk(self.root_dir):
            # Skip noise
            for ignore in [".git", "node_modules", "__pycache__", "dist", "build", ".venv"]:
                if ignore in dirs:
                    dirs.remove(ignore)

            rel_path = os.path.relpath(root, self.root_dir)
            if rel_path == ".": rel_path = ""
            
            for file in files:
                self.repo_map["metrics"]["total_files"] += 1
                full_path = os.path.join(root, file)
                
                # Tech stack detection
                if file in config_signatures:
                    stack = config_signatures[file]
                    if stack not in self.repo_map["tech_stack"]:
                        self.repo_map["tech_stack"].append(stack)
                
                # Dependency parsing
                if file == "package.json":
                    self._parse_npm(full_path)
                elif file == "requirements.txt":
                    self._parse_pip(full_path)

        # Check for gaps
        required = ["Dockerfile", ".github/workflows", "README.md", "LICENSE", ".env.example"]
        for req in required:
            found = any(f.endswith(req) or req in f for f in self._get_all_files())
            if not found:
                self.repo_map["missing_elements"].append(req)

        return self.repo_map

    def _get_all_files(self):
        all_files = []
        for root, dirs, files in os.walk(self.root_dir):
            if ".git" in dirs: dirs.remove(".git")
            for f in files:
                all_files.append(os.path.join(os.path.relpath(root, self.root_dir), f))
        return all_files

    def _parse_npm(self, path):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                self.repo_map["dependencies"]["npm"] = data.get("dependencies", {})
        except: pass

    def _parse_pip(self, path):
        try:
            with open(path, 'r') as f:
                deps = [line.split('==')[0].strip() for line in f if line.strip() and not line.startswith('#')]
                self.repo_map["dependencies"]["pip"] = deps
        except: pass

    def generate_report(self):
        m = self.repo_map
        report = f"# Repo Analysis Report - {m['meta']['timestamp']}\n\n"
        report += "## 🏗 Tech Stack\n"
        report += ", ".join(m['tech_stack']) if m['tech_stack'] else "Unknown"
        report += "\n\n## 📊 Metrics\n"
        report += f"- Total Files: {m['metrics']['total_files']}\n"
        
        report += "\n## 🚩 Missing Elements\n"
        for item in m['missing_elements']:
            report += f"- [ ] {item}\n"
            
        report += "\n## 📦 Dependencies\n"
        for mgr, deps in m['dependencies'].items():
            report += f"### {mgr}\n"
            report += f"- {len(deps)} dependencies detected.\n"
            
        return report

if __name__ == "__main__":
    analyzer = RepoAnalyzer()
    repo_map = analyzer.scan()
    with open("repo_map.json", "w") as f:
        json.dump(repo_map, f, indent=2)
    with open("analysis_report.md", "w") as f:
        f.write(analyzer.generate_report())
    print("✅ Analysis phase complete.")
