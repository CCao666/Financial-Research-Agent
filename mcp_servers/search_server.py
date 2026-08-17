import json

from ddgs import DDGS
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("local-web-search")


@mcp.tool()
def search_market_news(query: str, max_results: int = 5) -> str:
    """Search recent public web results for company news and market sentiment."""
    limit = min(max(max_results, 1), 8)
    results = list(DDGS().news(query=query, max_results=limit))
    normalized = [
        {
            "title": item.get("title"),
            "summary": item.get("body"),
            "url": item.get("url"),
            "date": item.get("date"),
            "publisher": item.get("source"),
        }
        for item in results
    ]
    return json.dumps(normalized, default=str)


if __name__ == "__main__":
    mcp.run(transport="stdio")

