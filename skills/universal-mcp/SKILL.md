# Universal MCP Factory
A dynamic system for generating and deploying Model Context Protocol (MCP) servers to bridge the AI with any external API or local service.

## Capabilities
- **API-to-MCP Translation**: Scrape API docs or OpenAPI specs to generate a functional MCP server.
- **Dynamic Server Registration**: Programmatically update `mcp_universal_config.json` to activate new tools.
- **Node/Python Generation**: Create servers in the most appropriate language for the target integration.
- **Safety Sandboxing**: Validate tool schemas before registration to prevent system instability.

## Usage
Input a service name and its API endpoint/specification to generate a new MCP integration.
