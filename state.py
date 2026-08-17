from operator import add
from typing import Annotated, Any, TypedDict


def merge_dicts(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    return {**left, **right}


class ResearchState(TypedDict, total=False):
    query: str
    plan: dict[str, Any]
    valid_tickers: list[str]
    invalid_tickers: list[str]
    agent_results: Annotated[dict[str, Any], merge_dicts]
    sources: Annotated[list[str], add]
    warnings: Annotated[list[str], add]
    errors: Annotated[list[str], add]
    execution_trace: Annotated[list[dict[str, str]], add]
    verification_passed: bool
    verification_status: str
    final_report: str
