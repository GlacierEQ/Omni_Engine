# Installation Request with OAuth Enabled

- **Command**
  - `npx -y install-mcp@latest https://api.supermemory.ai/mcp --client claude --oauth=yes`
- **Result**
  - Installation failed. The installer reported: `Authentication failed. Use the client to authenticate.`
- **Notes**
  - The MCP server requires an authentication flow when OAuth is enabled. Without completing the flow interactively, the installation does not proceed.
