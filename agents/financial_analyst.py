from langgraph.prebuilt import create_react_agent

from agents.common import last_text, model
from mcp_client import get_mcp_tools
from state import ResearchState

PROMPT = """You are a financial analyst. Use the financial MCP tool for every ticker in the
request. Compare only returned metrics, preserve units, identify missing data, and cite Yahoo
Finance in your answer. Never invent a metric."""


async def financial_analyst(state: ResearchState) -> dict:
    task = next(
        task for task in state["plan"]["tasks"] if task["agent"] == "financial_analyst"
    )
    valid = state.get("valid_tickers", [])
    invalid = state.get("invalid_tickers", [])
    if state["plan"].get("companies") and not valid:
        message = "No valid ticker remained after validation; financial analysis was not run."
        return {
            "agent_results": {"financial_analyst": {"status": "failed", "summary": message}},
            "errors": [message],
            "execution_trace": [{"node": "financial_analyst", "status": "failed"}],
        }

    instruction = (
        f"{task['instruction']}\nValid tickers: {valid or 'not explicitly specified'}. "
        f"Invalid tickers (do not query): {invalid or 'none'}."
    )
    try:
        async with get_mcp_tools("financial") as tools:
            agent = create_react_agent(model(), tools, prompt=PROMPT)
            result = await agent.ainvoke({"messages": [("user", instruction)]})
        summary = last_text(result["messages"])
        status = "partial" if invalid else "success"
        return {
            "agent_results": {"financial_analyst": {"status": status, "summary": summary}},
            "sources": ["Yahoo Finance via local Financial MCP server"],
            "execution_trace": [{"node": "financial_analyst", "status": status}],
        }
    except Exception as exc:  # noqa: BLE001 - MCP/network errors become graph state
        return {
            "agent_results": {"financial_analyst": {"status": "failed", "summary": str(exc)}},
            "errors": [f"Financial analyst failed: {exc}"],
            "execution_trace": [{"node": "financial_analyst", "status": "failed"}],
        }
