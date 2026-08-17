import asyncio
import os

import streamlit as st

from agent import agent

st.set_page_config(page_title="Financial Research Agent", page_icon="📈", layout="wide")
st.title("📈 Multi-Agent Financial Research")
st.caption("OpenAI + LangGraph + local Financial and Search MCP servers")

query = st.text_area(
    "Research question",
    "Compare NVDA and AMD in terms of valuation, growth, recent catalysts, and market sentiment.",
    height=100,
)

if st.button("Run analysis", type="primary", disabled=not query.strip()):
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY is missing. Copy .env.example to .env and add your key.")
        st.stop()

    with st.spinner("Specialist agents are researching in parallel..."):
        try:
            result = asyncio.run(
                agent.ainvoke(
                    {
                        "query": query.strip(),
                        "agent_results": {},
                        "valid_tickers": [],
                        "invalid_tickers": [],
                        "sources": [],
                        "warnings": [],
                        "errors": [],
                        "execution_trace": [],
                    }
                )
            )
        except Exception as exc:  # noqa: BLE001 - display graph failures in the UI
            st.exception(exc)
            st.stop()

    st.markdown(result.get("final_report", "No report was generated."))

    if result.get("warnings"):
        with st.expander("Warnings", expanded=True):
            for warning in result["warnings"]:
                st.warning(warning)

    with st.sidebar:
        st.header("Execution trace")
        for event in result.get("execution_trace", []):
            icon = (
                "✅"
                if event["status"] in {"completed", "success"}
                else "⏭️"
                if event["status"] == "skipped"
                else "⚠️"
            )
            st.write(f"{icon} `{event['node']}` — {event['status']}")
        with st.expander("Research plan"):
            st.json(result.get("plan", {}))
        with st.expander("Ticker validation"):
            st.json(
                {
                    "valid": result.get("valid_tickers", []),
                    "invalid": result.get("invalid_tickers", []),
                }
            )
