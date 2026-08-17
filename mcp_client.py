import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

ROOT = Path(__file__).resolve().parent


def server_config(server: str) -> dict:
    module_by_server = {
        "financial": "mcp_servers.financial_server",
        "search": "mcp_servers.search_server",
    }
    if server not in module_by_server:
        raise ValueError(f"Unknown MCP server: {server}")
    return {
        server: {
            "transport": "stdio",
            "command": sys.executable,
            "args": ["-m", module_by_server[server]],
            "cwd": str(ROOT),
        }
    }


@asynccontextmanager
async def get_mcp_tools(server: str) -> AsyncIterator[list[BaseTool]]:
    client = MultiServerMCPClient(server_config(server))
    tools = await client.get_tools()
    yield tools
