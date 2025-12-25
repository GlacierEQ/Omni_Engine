# AI LaTeX Paper Pipeline

```bash
# 1. Generate full IEEE paper
mcp overleaf ai_generate_paper '{"topic":"Transformers","sections":["intro","method","results"],"template":"ieee"}'

# 2. Create + compile project
project_id=$(mcp overleaf create_project '{"template":"ieee","title":"Transformer Research"}' | jq .project_id)

# 3. Compile PDF
mcp overleaf compile_pdf "{\"project_id\":\"$project_id\"}"

# 4. Export + Git commit
mcp overleaf export_pdf "{\"project_id\":\"$project_id\"}" > paper.pdf
git add paper.pdf && git commit -m "AI-generated paper"
```
