from agents.common import model
from state import ResearchState

PROMPT = """Answer the user's general financial education question clearly and concisely.
Do not imply that live data or external tools were used. This is educational information, not
personalized investment advice."""


async def direct_answer(state: ResearchState) -> dict:
    response = await model(0.1).ainvoke([("system", PROMPT), ("user", state["query"])])
    return {
        "final_report": str(response.content),
        "verification_passed": True,
        "verification_status": "success",
        "execution_trace": [{"node": "direct_answer", "status": "completed"}],
    }
