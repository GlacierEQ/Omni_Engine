# Omni_Engine → GitHub Actions Setup

## 1. Copy OpenAPI Spec
Copy contents of `omni_engine_github_openapi.yaml`

## 2. Custom GPT Setup
1. Go to https://chatgpt.com/gpts/editor → Create/Edit GPT
2. Actions → "Create new action"
3. Paste OpenAPI spec
4. Name: "GitHub Omni_Engine"
5. Description: "Read files, commit changes, open PRs, list repos"

## 3. Authentication
1. "Save & Authenticate"
2. Paste your GitHub Personal Access Token (PAT)
3. Scopes needed: `repo` (full control)

## 4. Test in GPT
Try: "List my repos" → should see github/list_repos in tools

## PAT Creation
https://github.com/settings/tokens → Generate new → Select `repo` scope

**Result**: GitHub appears permanently in your GPT tool menu.
