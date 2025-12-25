🔧 NOTION MCP TROUBLESHOOTING GUIDE

## Step 1: Get Notion Token
1. notion.com/my-integrations
2. New Integration → Name: "1FDV Court AI"
3. Copy Internal Integration Token

## Step 2: Connect MCP
mcp notion auth [paste_token_here]

## Step 3: Test
mcp notion list-databases

## Step 4: Your 1FDV Data
mcp notion query-database "1FDV Master"

