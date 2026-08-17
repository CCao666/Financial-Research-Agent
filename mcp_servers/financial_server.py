import json

import yfinance as yf
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("local-financial-data")


def _get_info(symbol: str) -> dict:
    try:
        return yf.Ticker(symbol).info or {}
    except Exception:  # noqa: BLE001 - normalize upstream provider failures
        return {}


@mcp.tool()
def validate_ticker(ticker: str) -> str:
    """Validate a public-company ticker before financial research."""
    symbol = ticker.strip().upper()
    info = _get_info(symbol)
    valid = bool(
        symbol
        and any(
            info.get(key) is not None
            for key in ("marketCap", "regularMarketPrice", "currentPrice", "longName")
        )
    )
    return json.dumps(
        {
            "ticker": symbol,
            "valid": valid,
            "company_name": info.get("longName") if valid else None,
            "error": None if valid else "No market data found.",
        }
    )


@mcp.tool()
def get_stock_metrics(ticker: str) -> str:
    """Return current valuation and growth metrics for a public-company ticker."""
    symbol = ticker.strip().upper()
    info = _get_info(symbol)
    if not info or not any(info.get(key) is not None for key in ("marketCap", "regularMarketPrice")):
        return json.dumps({"ticker": symbol, "error": "No market data found."})

    result = {
        "ticker": symbol,
        "company_name": info.get("longName"),
        "currency": info.get("currency"),
        "price": info.get("regularMarketPrice") or info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "trailing_pe": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "revenue_growth": info.get("revenueGrowth"),
        "profit_margin": info.get("profitMargins"),
        "fifty_two_week_change": info.get("52WeekChange"),
        "source": f"Yahoo Finance ({symbol})",
    }
    return json.dumps(result, default=str)


if __name__ == "__main__":
    mcp.run(transport="stdio")
