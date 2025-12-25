# MCP Server Setup Guide for All Platforms

## 🌟 Your Enhanced MCP Servers Are Ready!

**6 Servers | 26 Tools | Operator Code Connected**

---

## 📱 Platform-Specific Setup

### 1️⃣ ChatGPT Desktop App

**Configuration Location:**
- macOS: `~/Library/Application Support/com.openai.chat/Desktop/mcp_settings.json`
- Windows: `%APPDATA%\OpenAI\ChatGPT\Desktop\mcp_settings.json`
- Linux: `~/.config/OpenAI/ChatGPT/Desktop/mcp_settings.json`

**Setup Steps:**
```bash
# Copy the ChatGPT configuration
cp ~/mcp-integration/platform-configs/chatgpt-mcp-config.json ~/.config/OpenAI/ChatGPT/Desktop/mcp_settings.json

# Or create manually
mkdir -p ~/.config/OpenAI/ChatGPT/Desktop
```

**Required:**
- Update API keys in the configuration
- Restart ChatGPT Desktop app

---

### 2️⃣ Cline (VS Code Extension)

**Configuration Location:**
- VS Code Settings: Search for "Cline MCP"
- Or: `~/.vscode/settings.json`

**Setup Steps:**
```bash
# Add to VS Code settings
cat >> ~/.vscode/settings.json << 'EOF'

{
  "cline.mcpServers": {
    "jules2_enhanced": {
      "command": "node",
      "args": ["/home/user/mcp-integration/servers/jules2-server-enhanced.js"],
      "env": {
        "JULES_API_KEY": "your-jules-key",
        "OPERATOR_GUID": "OPR-NS8-GE8-KC3-001-AI-GRS-GUID:983DE8C8-E120-1-B5A0-C6D8AF97BB09"
      }
    }
    // ... add other servers as needed
  }
}
