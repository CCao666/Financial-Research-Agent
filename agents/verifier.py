from state import ResearchState


def verifier(state: ResearchState) -> dict:
    results = state.get("agent_results", {})
    selected = {
        task["agent"] for task in state.get("plan", {}).get("tasks", [])
    }
    selected_results = {name: results.get(name, {}) for name in selected}
    failed = [name for name, value in selected_results.items() if value.get("status") == "failed"]
    partial = [name for name, value in selected_results.items() if value.get("status") == "partial"]
    warnings = [f"{name} did not complete; the final report may be incomplete." for name in failed]
    warnings.extend(f"{name} returned partial results." for name in partial)
    succeeded = [
        name
        for name, value in selected_results.items()
        if value.get("status") in {"success", "partial"}
    ]
    passed = bool(succeeded)
    status = "failed" if not passed else "partial" if failed or partial or state.get("invalid_tickers") else "success"
    return {
        "verification_passed": passed,
        "verification_status": status,
        "warnings": warnings,
        "execution_trace": [{"node": "verifier", "status": status}],
    }
