#!/bin/bash
# NOTION CONNECTOR - SETUP SCRIPT
# Automated setup of SUPERNOVA Evidence Matrix and supporting databases
# For: OPERATOR + Kekoa TRO Case (1FDV-23-0001009)

set -e

echo "════════════════════════════════════════════════════════════════"
echo "  NOTION CONNECTOR SETUP - SUPERNOVA EVIDENCE MATRIX"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
WORKSPACE_ROOT_PAGE_ID="${1:-}"
if [ -z "$WORKSPACE_ROOT_PAGE_ID" ]; then
    echo -e "${RED}ERROR: Please provide workspace root page ID as first argument${NC}"
    echo "Usage: ./NOTION_SETUP_TEMPLATE.sh <root_page_id>"
    exit 1
fi

echo -e "${YELLOW}Step 1: Testing Notion connection...${NC}"
if mcp notion notion-search '{"query":"test"}' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Notion connection successful${NC}"
else
    echo -e "${RED}✗ Notion connection failed${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 2: Creating Master SUPERNOVA page...${NC}"

MASTER_PAGE=$(mcp notion notion-create-pages "{
  \"parent\": {\"page_id\": \"$WORKSPACE_ROOT_PAGE_ID\"},
  \"title\": \"SUPERNOVA Evidence Matrix - Kekoa TRO (1FDV-23-0001009)\",
  \"content\": \"# SUPERNOVA Evidence Matrix\\n\\nFull legal intelligence system for Case 1FDV-23-0001009 (Kekoa TRO)\\n\\n## Components\\n- Evidence Pieces (All collected evidence)\\n- Actor Network (Judges, attorneys, parties)\\n- Events Timeline (Chronological case events)\\n- Legal Statutes (Relevant laws and precedents)\\n- Strategic Analysis (Case strategy and outcomes)\\n\\n## Status: Initializing\\n\nGenerated: $(date)\"
}" 2>&1)

# Extract page ID from response (this is simplified - actual parsing needed)
MASTER_PAGE_ID=$(echo "$MASTER_PAGE" | grep -oP '(?<=\"id\": \")[^\"]*' | head -1)
echo -e "${GREEN}✓ Master page created: $MASTER_PAGE_ID${NC}"

echo ""
echo -e "${YELLOW}Step 3: Creating Evidence Database...${NC}"

EVIDENCE_DB=$(mcp notion notion-create-database "{
  \"parent\": {\"page_id\": \"$MASTER_PAGE_ID\"},
  \"title\": \"Evidence Pieces\",
  \"properties\": {
    \"Type\": {\"type\": \"select\", \"select\": {\"options\": [
      {\"name\": \"Document\", \"color\": \"blue\"},
      {\"name\": \"Testimony\", \"color\": \"green\"},
      {\"name\": \"Communication\", \"color\": \"purple\"},
      {\"name\": \"Metadata\", \"color\": \"yellow\"},
      {\"name\": \"Forensic\", \"color\": \"red\"}
    ]}},
    \"Source\": {\"type\": \"rich_text\"},
    \"Date_Collected\": {\"type\": \"date\"},
    \"Key_Content\": {\"type\": \"rich_text\"},
    \"Legal_Relevance\": {\"type\": \"select\", \"select\": {\"options\": [
      {\"name\": \"Critical (HRS §586)\", \"color\": \"red\"},
      {\"name\": \"Supporting\", \"color\": \"orange\"},
      {\"name\": \"Context\", \"color\": \"yellow\"},
      {\"name\": \"Precedent\", \"color\": \"blue\"}
    ]}},
    \"Forensic_Integrity\": {\"type\": \"checkbox\"},
    \"Blockchain_Hash\": {\"type\": \"rich_text\"},
    \"Analysis_Notes\": {\"type\": \"rich_text\"}
  }
}" 2>&1)

EVIDENCE_DB_ID=$(echo "$EVIDENCE_DB" | grep -oP '(?<=\"id\": \")[^\"]*' | head -1)
echo -e "${GREEN}✓ Evidence database created: $EVIDENCE_DB_ID${NC}"

echo ""
echo -e "${YELLOW}Step 4: Creating Actor Network Database...${NC}"

ACTOR_DB=$(mcp notion notion-create-database "{
  \"parent\": {\"page_id\": \"$MASTER_PAGE_ID\"},
  \"title\": \"Actor Network\",
  \"properties\": {
    \"Role\": {\"type\": \"select\", \"select\": {\"options\": [
      {\"name\": \"Judge\", \"color\": \"red\"},
      {\"name\": \"Attorney\", \"color\": \"orange\"},
      {\"name\": \"Party\", \"color\": \"green\"},
      {\"name\": \"Witness\", \"color\": \"blue\"},
      {\"name\": \"Organization\", \"color\": \"purple\"}
    ]}},
    \"Case_Role\": {\"type\": \"rich_text\"},
    \"Key_Behaviors\": {\"type\": \"rich_text\"},
    \"Bias_Indicators\": {\"type\": \"select\", \"select\": {\"options\": [
      {\"name\": \"None_Detected\", \"color\": \"green\"},
      {\"name\": \"Possible\", \"color\": \"yellow\"},
      {\"name\": \"Probable\", \"color\": \"orange\"},
      {\"name\": \"Confirmed\", \"color\": \"red\"}
    ]}},
    \"Misconduct_Flags\": {\"type\": \"checkbox\"},
    \"Strategic_Analysis\": {\"type\": \"rich_text\"}
  }
}" 2>&1)

ACTOR_DB_ID=$(echo "$ACTOR_DB" | grep -oP '(?<=\"id\": \")[^\"]*' | head -1)
echo -e "${GREEN}✓ Actor database created: $ACTOR_DB_ID${NC}"

echo ""
echo -e "${YELLOW}Step 5: Creating Events Timeline Database...${NC}"

TIMELINE_DB=$(mcp notion notion-create-database "{
  \"parent\": {\"page_id\": \"$MASTER_PAGE_ID\"},
  \"title\": \"Events Timeline\",
  \"properties\": {
    \"Event_Type\": {\"type\": \"select\", \"select\": {\"options\": [
      {\"name\": \"Court_Filing\", \"color\": \"red\"},
      {\"name\": \"Communication\", \"color\": \"blue\"},
      {\"name\": \"Incident\", \"color\": \"orange\"},
      {\"name\": \"Ruling\", \"color\": \"purple\"},
      {\"name\": \"Evidence_Acquisition\", \"color\": \"green\"}
    ]}},
    \"Date\": {\"type\": \"date\"},
    \"Key_Details\": {\"type\": \"rich_text\"},
    \"Strategic_Significance\": {\"type\": \"select\", \"select\": {\"options\": [
      {\"name\": \"High\", \"color\": \"red\"},
      {\"name\": \"Medium\", \"color\": \"orange\"},
      {\"name\": \"Low\", \"color\": \"gray\"}
    ]}},
    \"Causality_Chain\": {\"type\": \"rich_text\"}
  }
}" 2>&1)

TIMELINE_DB_ID=$(echo "$TIMELINE_DB" | grep -oP '(?<=\"id\": \")[^\"]*' | head -1)
echo -e "${GREEN}✓ Timeline database created: $TIMELINE_DB_ID${NC}"

echo ""
echo -e "${YELLOW}Step 6: Creating Legal Statutes Database...${NC}"

LEGAL_DB=$(mcp notion notion-create-database "{
  \"parent\": {\"page_id\": \"$MASTER_PAGE_ID\"},
  \"title\": \"Legal Statutes & Precedents\",
  \"properties\": {
    \"Category\": {\"type\": \"select\", \"select\": {\"options\": [
      {\"name\": \"Primary_Statute\", \"color\": \"red\"},
      {\"name\": \"Related_Statute\", \"color\": \"blue\"},
      {\"name\": \"Favorable_Precedent\", \"color\": \"green\"},
      {\"name\": \"Adverse_Precedent\", \"color\": \"orange\"}
    ]}},
    \"Text\": {\"type\": \"rich_text\"},
    \"Relevance_To_Case\": {\"type\": \"rich_text\"},
    \"Application_Strategy\": {\"type\": \"rich_text\"}
  }
}" 2>&1)

LEGAL_DB_ID=$(echo "$LEGAL_DB" | grep -oP '(?<=\"id\": \")[^\"]*' | head -1)
echo -e "${GREEN}✓ Legal statutes database created: $LEGAL_DB_ID${NC}"

echo ""
echo -e "${YELLOW}Step 7: Creating Strategic Analysis Page...${NC}"

STRATEGY_PAGE=$(mcp notion notion-create-pages "{
  \"parent\": {\"page_id\": \"$MASTER_PAGE_ID\"},
  \"title\": \"Strategic Analysis\",
  \"content\": \"# Strategic Analysis - Kekoa TRO Case\\n\\n## Judge Naso Disqualification Strategy\\n(To be populated by bias documentation)\\n\\n## Attorney Brower Misconduct Case\\n(To be populated by ethics analysis)\\n\\n## Evidence Weaponization\\n(To be populated by SUPERNOVA matrix)\\n\\n## Predicted Outcomes\\n\\n### Optimistic\\n\\n### Realistic\\n\\n### Pessimistic\\n\"
}" 2>&1)

echo -e "${GREEN}✓ Strategic analysis page created${NC}"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✓ SETUP COMPLETE${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Notion Workspace Created:"
echo "  Master Page: $MASTER_PAGE_ID"
echo "  Evidence DB: $EVIDENCE_DB_ID"
echo "  Actor DB: $ACTOR_DB_ID"
echo "  Timeline DB: $TIMELINE_DB_ID"
echo "  Legal DB: $LEGAL_DB_ID"
echo ""
echo "Next Steps:"
echo "  1. Open master page in Notion: https://notion.so/$MASTER_PAGE_ID"
echo "  2. Verify all 5 databases are visible"
echo "  3. Populate test data (3-5 entries per database)"
echo "  4. Test bi-directional Supermemory sync"
echo "  5. Deploy n8n automation workflows"
echo ""
echo "Documentation: ~/NOTION_CONNECTOR_GUIDE.md"
echo ""

