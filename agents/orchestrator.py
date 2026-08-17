from agents.common import model
from models.research import ResearchPlan
from state import ResearchState

PROMPT = """Create a concise routing plan for the user's financial question.

- companies must contain uppercase exchange ticker symbols, not company names. Resolve common
  names such as Apple to AAPL and Tesla to TSLA.
- Assign metrics, valuation, growth, profitability, price, or financial comparisons to
  financial_analyst.
- Assign news, catalysts, events, risks, or sentiment to market_researcher.
- Include both only when the request genuinely needs both categories.
- For educational questions that do not need current company data, use task_type=general and no
  specialist tasks.
- Never add a specialist merely to make the plan look comprehensive.

Return only the requested structured data."""


async def orchestrator(state: ResearchState) -> dict:
    planner = model(0).with_structured_output(ResearchPlan)
    plan = await planner.ainvoke([("system", PROMPT), ("user", state["query"])])
    return {
        "plan": plan.model_dump(),
        "execution_trace": [{"node": "orchestrator", "status": "completed"}],
    }
