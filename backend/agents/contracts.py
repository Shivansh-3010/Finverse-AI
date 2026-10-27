from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AgentStatus(StrEnum):
    SUCCESS = "success"
    PARTIAL = "partial"
    SKIPPED = "skipped"
    FAILED = "failed"


class AgentResult(BaseModel):
    """Standardized result returned by a FinVerse AI agent."""

    model_config = ConfigDict(extra="forbid")

    agent_name: str = Field(min_length=1)
    status: AgentStatus
    data: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
