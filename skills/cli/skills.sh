#!/bin/bash
# 🚀 SKILLS CLI WRAPPER
# Quick access to skills orchestrator

SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Add to PATH for easy access
export PATH="${SKILLS_DIR}/cli:$PATH"

# Main command
python3 "${SKILLS_DIR}/cli/skills.py" "$@"
