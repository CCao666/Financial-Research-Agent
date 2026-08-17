from agents.common import model
from state import ResearchState

PROMPT = """Write an executive financial research brief using only the supplied specialist
results. Include: Executive Summary, Financial Comparison, Market Sentiment and Catalysts, Risks
and Limitations, and Sources. Clearly disclose missing or failed research. Never add unsupported
facts. This is research, not personalized investment advice."""


async def report_writer(state: ResearchState) -> dict:
    payload = {
        "question": state["query"],
        "specialist_results": state.get("agent_results", {}),
        "valid_tickers": state.get("valid_tickers", []),
        "invalid_tickers": state.get("invalid_tickers", []),
        "verification_status": state.get("verification_status"),
        "known_sources": state.get("sources", []),
        "warnings": state.get("warnings", []),
        "errors": state.get("errors", []),
    }
    response = await model(0.1).ainvoke([("system", PROMPT), ("user", str(payload))])
    return {
        "final_report": str(response.content),
        "execution_trace": [{"node": "report_writer", "status": "completed"}],
    }
