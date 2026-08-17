import json
import re

from mcp_client import get_mcp_tools
from state import ResearchState

SPECIALISTS = ("financial_analyst", "market_researcher")
NON_TICKER_ACRONYMS = {
    "CEO",
    "CFO",
    "EPS",
    "ETF",
    "GDP",
    "LLM",
    "MCP",
    "NASDAQ",
    "NYSE",
    "RAG",
    "SEC",
    "USD",
}


def selected_agents(plan: dict) -> set[str]:
    return {task["agent"] for task in plan.get("tasks", [])}


def ticker_candidates(query: str) -> list[str]:
    """Extract explicit uppercase ticker-like tokens without relying on the planner."""
    tokens = re.findall(
        r"(?<![A-Z0-9.-])[A-Z][A-Z0-9]{1,9}(?:[.-][A-Z0-9]+)?(?![A-Z0-9.-])",
        query,
    )
    return [token for token in tokens if token not in NON_TICKER_ACRONYMS]


def parse_mcp_json(value: object) -> dict:
    """Normalize JSON returned as text or LangChain MCP content blocks."""
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        return json.loads(value)
    if isinstance(value, list):
        for block in value:
            if isinstance(block, dict) and block.get("type") == "text":
                return json.loads(block["text"])
    raise ValueError(f"Unsupported MCP response type: {type(value).__name__}")


async def input_validator(state: ResearchState) -> dict:
    plan = state["plan"]
    selected = selected_agents(plan)
    skipped = set(SPECIALISTS) - selected
    planned = [ticker.strip().upper() for ticker in plan.get("companies", [])]
    companies = list(dict.fromkeys([*planned, *ticker_candidates(state["query"])]))

    valid: list[str] = []
    invalid: list[str] = []
    warnings: list[str] = []

    if companies:
        try:
            async with get_mcp_tools("financial") as tools:
                validator = next(tool for tool in tools if tool.name == "validate_ticker")
                for ticker in companies:
                    raw = await validator.ainvoke({"ticker": ticker})
                    result = parse_mcp_json(raw)
                    (valid if result.get("valid") else invalid).append(ticker)
        except Exception as exc:  # noqa: BLE001 - validation failure is reported in graph state
            warnings.append(f"Ticker validation unavailable: {exc}")
            valid = companies

    if invalid:
        warnings.append(f"Invalid or unavailable ticker(s): {', '.join(invalid)}.")

    skipped_results = {
        name: {"status": "skipped", "summary": "Not selected by the orchestrator."}
        for name in skipped
    }
    skipped_trace = [{"node": name, "status": "skipped"} for name in sorted(skipped)]

    return {
        "valid_tickers": valid,
        "invalid_tickers": invalid,
        "agent_results": skipped_results,
        "warnings": warnings,
        "execution_trace": [
            {"node": "input_validator", "status": "completed"},
            *skipped_trace,
        ],
    }
