from agents.verifier import verifier


def test_partial_result_still_passes_with_partial_status():
    result = verifier(
        {
            "plan": {
                "tasks": [
                    {"agent": "financial_analyst", "instruction": "compare"},
                ]
            },
            "agent_results": {
                "financial_analyst": {"status": "partial", "summary": "AAPL only"},
                "market_researcher": {"status": "skipped", "summary": "not selected"},
            },
            "invalid_tickers": ["INVALIDXYZ"],
        }
    )
    assert result["verification_passed"] is True
    assert result["verification_status"] == "partial"


def test_all_selected_agents_failed():
    result = verifier(
        {
            "plan": {
                "tasks": [{"agent": "financial_analyst", "instruction": "compare"}]
            },
            "agent_results": {
                "financial_analyst": {"status": "failed", "summary": "no data"}
            },
            "invalid_tickers": ["INVALIDXYZ"],
        }
    )
    assert result["verification_passed"] is False
    assert result["verification_status"] == "failed"
