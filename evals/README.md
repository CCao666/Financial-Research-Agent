# LLM-as-a-Judge evaluation

The suite runs ten questions through the complete graph and grades three primary metrics:

1. **Router accuracy** — expected agents/tickers versus actual routing and ticker validation.
2. **Relevance** — coverage of the requested analysis without material digressions.
3. **Groundedness** — whether final-answer claims are supported by specialist/MCP evidence.

Groundedness measures faithfulness to the captured evidence. It is not independent fact-checking
of Yahoo Finance or the linked news pages.

Run a cheap one-case smoke evaluation first:

```bash
uv run python -m evals.run_eval --limit 1
```

Then run all ten cases:

```bash
uv run python -m evals.run_eval
```

Use a separate judge model if desired:

```bash
JUDGE_MODEL=gpt-4o-mini uv run python -m evals.run_eval
```

Results are written to `evals/results/latest.json` and `evals/results/latest.md`. A case passes
only when deterministic route and ticker checks both pass, no critical failure is detected, and
all three Judge scores meet the default 4/5 threshold.

