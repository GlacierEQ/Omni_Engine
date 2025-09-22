# Unsupported Client Attempt

- **Command**
  - `npx -y install-mcp@latest https://api.supermemory.ai/mcp --client codex --oauth=yes`
- **Result**
  - Installation aborted. The installer responded: `Invalid client "codex". Supported clients: claude`.
- **Notes**
  - The `codex` client type is not recognized. Installation must use a supported client such as `claude`.
