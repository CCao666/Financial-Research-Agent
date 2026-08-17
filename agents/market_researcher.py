from langgraph.prebuilt import create_react_agent

from agents.common import last_text, model
from mcp_client import get_mcp_tools
from state import ResearchState

PROMPT = """You are a market-news researcher. Use the search MCP tool before answering.
Summarize recent catalysts, risks, and sentiment. Distinguish facts from your interpretation and
include the URLs returned by the tool. Do not fabricate headlines or sources."""


async def market_researcher(state: ResearchState) -> dict:
    task = next(
        task for task in state["plan"]["tasks"] if task["agent"] == "market_researcher"
    )
    valid = state.get("valid_tickers", [])
    invalid = state.get("invalid_tickers", [])
    instruction = (
        f"{task['instruction']}\nValidated tickers: {valid or 'not explicitly specified'}. "
        f"Do not make claims about invalid tickers: {invalid or 'none'}."
    )
    try:
        async with get_mcp_tools("search") as tools:
            agent = create_react_agent(model(), tools, prompt=PROMPT)
            result = await agent.ainvoke({"messages": [("user", instruction)]})
        summary = last_text(result["messages"])
        status = "partial" if invalid and not valid else "success"
        return {
            "agent_results": {"market_researcher": {"status": status, "summary": summary}},
            "execution_trace": [{"node": "market_researcher", "status": status}],
        }
    except Exception as exc:  # noqa: BLE001 - MCP/network errors become graph state
        return {
            "agent_results": {"market_researcher": {"status": "failed", "summary": str(exc)}},
            "errors": [f"Market researcher failed: {exc}"],
            "execution_trace": [{"node": "market_researcher", "status": "failed"}],
        }
