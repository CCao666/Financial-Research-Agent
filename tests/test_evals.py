from pathlib import Path

from evals.run_eval import active_agents, exact_route_match, load_cases


def test_eval_dataset_has_ten_unique_cases():
    path = Path(__file__).parents[1] / "evals" / "questions.jsonl"
    cases = load_cases(path)
    assert len(cases) == 10
    assert len({case["id"] for case in cases}) == 10


def test_active_agents_excludes_skipped_nodes():
    trace = [
        {"node": "financial_analyst", "status": "skipped"},
        {"node": "market_researcher", "status": "success"},
        {"node": "verifier", "status": "success"},
    ]
    assert active_agents(trace) == ["market_researcher"]


def test_route_match_is_order_independent():
    assert exact_route_match(
        ["financial_analyst", "market_researcher"],
        ["market_researcher", "financial_analyst"],
    )
