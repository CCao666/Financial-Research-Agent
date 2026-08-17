from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph

from agents.direct_answer import direct_answer
from agents.financial_analyst import financial_analyst
from agents.input_validator import input_validator, selected_agents
from agents.market_researcher import market_researcher
from agents.orchestrator import orchestrator
from agents.report_writer import report_writer
from agents.verifier import verifier
from state import ResearchState

load_dotenv()

workflow = StateGraph(ResearchState)
workflow.add_node("orchestrator", orchestrator)
workflow.add_node("input_validator", input_validator)
workflow.add_node("financial_analyst", financial_analyst)
workflow.add_node("market_researcher", market_researcher)
workflow.add_node("direct_answer", direct_answer)
workflow.add_node("verifier", verifier)
workflow.add_node("report_writer", report_writer)

workflow.add_edge(START, "orchestrator")
workflow.add_edge("orchestrator", "input_validator")


def route_after_validation(state: ResearchState) -> list[str]:
    selected = selected_agents(state["plan"])
    if not selected:
        return ["direct_answer"]
    return sorted(selected)


workflow.add_conditional_edges(
    "input_validator",
    route_after_validation,
    ["financial_analyst", "market_researcher", "direct_answer"],
)
workflow.add_edge("financial_analyst", "verifier")
workflow.add_edge("market_researcher", "verifier")
workflow.add_edge("direct_answer", END)
workflow.add_edge("verifier", "report_writer")
workflow.add_edge("report_writer", END)

agent = workflow.compile()
