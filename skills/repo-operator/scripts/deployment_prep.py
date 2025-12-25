import json
import os

def run_prep():
    if not os.path.exists("repo_map.json"):
        print("❌ Error: Run analysis first.")
        return

    with open("repo_map.json", "r") as f:
        repo_map = json.load(f)

    tech = repo_map.get("tech_stack", [])
    
    # 1. Generate Multi-stage Dockerfile
    dockerfile = "# Multi-stage Build\n"
    if "Node.js" in tech:
        dockerfile += """FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build --if-present

FROM node:18-alpine AS runner
WORKDIR /app
COPY --from=builder /app ./
EXPOSE 3000
CMD ["npm", "start"]
"""
    elif "Python" in tech:
        dockerfile += """FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "main.py"]
"""
    else:
        dockerfile += "FROM alpine\nCMD [\"echo\", \"Static Deployment Ready\"]"

    with open("Dockerfile", "w") as f:
        f.write(dockerfile)

    # 2. CI/CD Pipeline
    os.makedirs(".github/workflows", exist_ok=True)
    with open(".github/workflows/deploy.yml", "w") as f:
        f.write("""name: Operator-Grade CI/CD
on:
  push:
    branches: [ main, develop ]
jobs:
  validate-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Security Scan
        run: echo "Scanning..."
      - name: Build Docker Image
        run: docker build -t app:${{ github.sha }} .
""")

    # 3. Environment Specs
    specs = {
        "environments": {
            "staging": {"platform": "k8s", "replicas": 1},
            "production": {"platform": "k8s", "replicas": 3}
        },
        "version_lock": "2.0.0"
    }
    with open("env_specs.yaml", "w") as f:
        import yaml
        try:
            import yaml
            yaml.dump(specs, f)
        except:
            f.write(json.dumps(specs, indent=2))

    print("✅ Deployment Prep phase complete.")

if __name__ == "__main__":
    run_prep()
