from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json


@dataclass
class MCPServerInfo:
    """Information about an MCP server installation."""

    name: str
    endpoint: str
    client: str
    status: str
    functions: list[str]


def build_catalog() -> dict[str, dict]:
    """Return a catalog of known MCP servers and their capabilities."""
    servers = [
        MCPServerInfo(
            name="filesystem",
            endpoint="@modelcontextprotocol/server-filesystem",
            client="claude",
            status="installed",
            functions=[
                "read_file",
                "write_file",
                "list_directory",
                "search_files",
                "move_file",
                "create_directory",
            ],
        ),
        MCPServerInfo(
            name="api-supermemory-ai",
            endpoint="https://api.supermemory.ai/mcp",
            client="claude",
            status="installed",
            functions=[
                "memory.create",
                "memory.query",
                "memory.delete",
            ],
        ),
        MCPServerInfo(
            name="api-supermemory-ai-oauth",
            endpoint="https://api.supermemory.ai/mcp",
            client="claude",
            status="auth_failed",
            functions=[],
        ),
        MCPServerInfo(
            name="api-supermemory-ai-codex",
            endpoint="https://api.supermemory.ai/mcp",
            client="codex",
            status="client_invalid",
            functions=[],
        ),
    ]
    return {info.name: asdict(info) for info in servers}


def save_catalog(path: Path) -> None:
    """Write the catalog as JSON to *path*."""
    catalog = build_catalog()
    path.write_text(json.dumps(catalog, indent=2))


if __name__ == "__main__":
    save_catalog(Path("docs/mcp/catalog.json"))
