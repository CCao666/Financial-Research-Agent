from typing import Literal

from pydantic import BaseModel, Field


class ResearchTask(BaseModel):
    agent: Literal["financial_analyst", "market_researcher"]
    instruction: str


class ResearchPlan(BaseModel):
    """A routing plan. Companies must contain exchange ticker symbols, not names."""

    companies: list[str] = Field(default_factory=list)
    task_type: Literal["single_company", "comparison", "market_research", "general"]
    tasks: list[ResearchTask] = Field(default_factory=list)


class AgentFinding(BaseModel):
    agent: str
    status: Literal["success", "partial", "failed", "skipped"]
    summary: str
    sources: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
