from agent import route_after_validation
from agents.input_validator import parse_mcp_json, ticker_candidates


def state_with(*agents: str) -> dict:
    return {
        "plan": {
            "tasks": [
                {"agent": agent, "instruction": "test"}
                for agent in agents
            ]
        }
    }


def test_market_only_routes_only_to_market_researcher():
    assert route_after_validation(state_with("market_researcher")) == ["market_researcher"]


def test_financial_only_routes_only_to_financial_analyst():
    assert route_after_validation(state_with("financial_analyst")) == ["financial_analyst"]


def test_combined_request_routes_to_both_specialists():
    assert route_after_validation(
        state_with("financial_analyst", "market_researcher")
    ) == ["financial_analyst", "market_researcher"]


def test_general_question_routes_to_direct_answer():
    assert route_after_validation(state_with()) == ["direct_answer"]


def test_explicit_invalid_ticker_is_not_silently_dropped():
    assert ticker_candidates("Compare INVALIDXYZ with AAPL on valuation.") == [
        "INVALIDXYZ",
        "AAPL",
    ]


def test_common_financial_acronyms_are_not_ticker_candidates():
    assert ticker_candidates("Explain EPS and SEC filings using an LLM.") == []


def test_mcp_content_blocks_are_parsed():
    assert parse_mcp_json(
        [{"type": "text", "text": '{"ticker":"AAPL","valid":true}'}]
    ) == {"ticker": "AAPL", "valid": True}
