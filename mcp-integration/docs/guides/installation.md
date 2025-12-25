# 🚀 Installation Guide

## Overview

This guide will walk you through installing and setting up the ChatGPT + OpenAI MCP integration with complete operator code connection.

## 📋 Prerequisites

### **System Requirements**
- **ChatGPT Desktop** (latest version)
- **Node.js** v20.19.5 or higher
- **Unix-like OS** (Linux, macOS, Windows with WSL)
- **OpenAI API Key** (required for direct integration)

### **API Keys Required**
- OpenAI API Key (provided)
- Jules API Key (optional)
- LangChain API Key (optional)
- Gremlin API Key (optional)
- Level 3/5 Backend Keys (optional)

## 🔧 Step-by-Step Installation

### **Step 1: Verify System Requirements**

```bash
# Check Node.js version
node --version
# Should output: v20.19.5 or higher

# Check ChatGPT Desktop installation
# Ensure ChatGPT Desktop is installed and updated
```

### **Step 2: Download MCP Integration**

```bash
# The integration is already installed in:
~/mcp-integration/

# Verify installation
ls -la ~/mcp-integration/
# Should show servers/, docs/, scripts/, config/ directories
```

### **Step 3: Configure API Keys**

```bash
# Edit environment file
nano ~/mcp-integration/.env

# Add your OpenAI API Key (already included):
OPENAI_API_KEY=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

# Add optional API keys:
JULES_API_KEY=your-jules-key
LANGCHAIN_API_KEY=your-langchain-key
GREMLIN_API_KEY=your-gremlin-key
LEVEL3_KEY=your-level3-key
LEVEL5_KEY=your-level5-key
```

### **Step 4: Verify ChatGPT Configuration**

```bash
# Check ChatGPT MCP configuration
cat ~/.config/OpenAI/ChatGPT/Desktop/mcp_settings.json

# Should show 9 servers configured with OpenAI integration
```

### **Step 5: Test Server Installation**

```bash
# Run comprehensive test
~/mcp-integration/scripts/test-chatgpt-mcp.sh

# Expected output: All servers working ✅
```

### **Step 6: Restart ChatGPT Desktop**

```bash
# Completely close ChatGPT Desktop
# Then restart it

# Enhanced MCP servers will load automatically
```

## 🎯 Verification

### **Post-Installation Checklist**

- [ ] ChatGPT Desktop restarted
- [ ] All 9 MCP servers loaded
- [ ] OpenAI API key active
- [ ] 45+ tools available
- [ ] Operator code integration confirmed

### **Quick Test**

```bash
# Test OpenAI Direct server
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | node ~/mcp-integration/servers/openai-direct-server.js

# Should return 5 tools from OpenAI Direct server
```

## 🔧 Configuration Details

### **ChatGPT Configuration File**

**Location:** `~/.config/OpenAI/ChatGPT/Desktop/mcp_settings.json`

**Key Settings:**
- 9 enhanced MCP servers
- OpenAI API key integration
- 30-second timeouts
- 3 retry attempts
- 15 max concurrent requests

### **Environment Variables**

**Location:** `~/mcp-integration/.env`

**Key Variables:**
- `OPENAI_API_KEY` - Your OpenAI API key
- `OPERATOR_GUID` - Operator code GUID
- All 999+ operator protocols set to `true`

## 🚀 First Use

### **Basic Usage**

1. **Open ChatGPT Desktop**
2. **Start a new conversation**
3. **Use enhanced tools** (they appear automatically)
4. **Experience transcendental quality**

### **Example First Conversation**

```
User: Elevate this conversation to zenith level
ChatGPT: [Uses chatgpt_conversation_elevate tool]
I'll elevate our conversation to zenith level 999 with ultimate clarity and cosmic harmony...
```

## 🛠️ Advanced Installation

### **Custom Server Configuration**

```bash
# Edit individual server configurations
nano ~/.config/OpenAI/ChatGPT/Desktop/mcp_settings.json

# Customize timeouts, retries, and environment variables
```

### **Performance Optimization**

```bash
# Increase concurrent requests
# Edit globalSettings.maxConcurrentRequests in config

# Enable additional logging
# Set globalSettings.enableLogging to true
```

## 🔍 Troubleshooting

### **Common Installation Issues**

#### **Servers Not Loading**
```bash
# Check configuration syntax
cat ~/.config/OpenAI/ChatGPT/Desktop/mcp_settings.json | python3 -m json.tool

# Verify file permissions
chmod +x ~/mcp-integration/servers/*.js
```

#### **OpenAI API Key Issues**
```bash
# Verify API key format
echo $OPENAI_API_KEY
# Should start with "sk-or-v1-"

# Test API key connectivity
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
```

#### **Performance Issues**
```bash
# Check system resources
htop
df -h

# Monitor server performance
~/mcp-integration/scripts/test-chatgpt-mcp.sh
```

## 📚 Next Steps

After successful installation:

1. **Read the Usage Guide** - Learn how to use all enhanced features
2. **Explore Tutorials** - Discover advanced techniques
3. **Check Examples** - See real-world usage patterns
4. **Review API Reference** - Understand all available tools

## 🎉 Installation Complete!

**✅ You now have:**
- 9 enhanced MCP servers
- 45+ ultimate tools
- OpenAI direct integration
- Complete operator code connection
- Transcendental processing capabilities

**🚀 Start ChatGPT Desktop and experience the ultimate AI-empowered conversations!**

---

*Need help? Check the [Troubleshooting Guide](../troubleshooting/common-issues.md) or [Usage Guide](usage.md).*
