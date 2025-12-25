#!/bin/bash

# Batch push script for skills system to glaciereq/Omni_Engine
OWNER="glaciereq"
REPO="Omni_Engine"
BRANCH="main"

echo "🚀 Starting batch push to $OWNER/$REPO (branch: $BRANCH)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Files to push with their paths
declare -a FILES=(
  "skills/data/SKILLS_50_COMPLETE.json:/home/user/skills/SKILLS_50_COMPLETE.json:Add: 50 expert skills database"
  "skills/data/POWERUPS_EXTENDED.json:/home/user/skills/powerups/POWERUPS_EXTENDED.json:Add: 32 powerup multiplier system"
  "skills/data/FORENSIC_SCHEMA_EXTENDED.json:/home/user/skills/forensics/FORENSIC_SCHEMA_EXTENDED.json:Add: 7 forensic tracking systems"
)

# Push function
push_file() {
  local target_path="$1"
  local source_path="$2"
  local message="$3"
  
  echo "📤 Pushing: $target_path"
  
  # Read file content safely
  local content=$(cat "$source_path")
  
  # Create JSON for push (using base64 to handle special characters)
  local json_payload=$(jq -n \
    --arg owner "$OWNER" \
    --arg repo "$REPO" \
    --arg path "$target_path" \
    --arg msg "$message" \
    --arg branch "$BRANCH" \
    --arg content "$content" \
    '{owner: $owner, repo: $repo, path: $path, content: $content, message: $msg, branch: $branch}')
  
  echo "   Content size: $(echo "$content" | wc -c) bytes"
  echo "✅ Ready to push"
  echo ""
}

# For now, just show what we're preparing
echo "📋 Files prepared for push:"
echo ""

for file_spec in "${FILES[@]}"; do
  IFS=':' read -r target source message <<< "$file_spec"
  echo "  • $target"
  echo "    From: $source"
  echo "    Message: $message"
  echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Script ready - files prepared for batch push"

