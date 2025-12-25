#!/bin/bash
# Deployment script for VLEX Integration

echo "Starting deployment of VLEX integration..."

# 1. Install dependencies
pip install requests

# 2. Set up environment variables
if [ -f .env ]; then
  source .env
fi

if [ -z "$VLEX_API_KEY" ]; then
  echo "Error: VLEX_API_KEY is not set."
  exit 1
fi

# 3. Verify installation
python3 -c "from skills.integrations.vlex.vlex_client import VlexClient; print('VlexClient loaded successfully')"

echo "Deployment complete."
