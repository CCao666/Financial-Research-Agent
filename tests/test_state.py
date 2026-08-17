from state import merge_dicts


def test_parallel_agent_results_are_merged():
    left = {"financial_analyst": {"status": "success"}}
    right = {"market_researcher": {"status": "success"}}
    assert merge_dicts(left, right) == {**left, **right}

