
# Local Notion MCP Server Setup (Integrated Template)

**Tags:** #integration #notion #cursor #claude #localserver #devops #template

---

## Purpose
Quick-start configuration block to locally run the Notion MCP server for Cursor or Claude Desktop.

---

## Ritual: Local Notion MCP Server Setup

### 1. Install Global Dependency
```bash
npm install -g @notionhq/notion-mcp-server
```

### 2. Create Config File
Paste the following JSON into `.cursor/mcp.json` (for Cursor) **or** `claude_desktop_config.json` (for Claude Desktop):

```json
{
  "mcpServers": {
    "notionApi": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "OPENAPI_MCP_HEADERS": "{\"Authorization\": \"Bearer ntn_YOUR_SECRET_HERE\", \"Notion-Version\": \"2022-06-28\"}"
      }
    }
  }
}
```

> Replace `ntn_YOUR_SECRET_HERE` with your personal Notion integration token.

### 3. Optional: Use Updated Notion API Version
Check [Notion API changelog](https://developers.notion.com/changelog) for latest versions.

### 4. Verification
Run your app or reload your dev environment; the local MCP server should now proxy Notion API requests.

---

## Notes & Best Practices
- Store your `ntn_` secret securely; do not hard-code in production repositories.
- Consider `.env` file usage or secure vault integrations.
- Recommended for internal tools, prototypes, and testing environments.

---

## Callout Block (for reuse)
```
[[ Local Notion MCP Server Config Template ]]
```

---

**Created by:** Notion Master Omniprompt  
**Domain:** Project Atlas → DevOps Codex  
**Version:** v1.0 (May 2025)
