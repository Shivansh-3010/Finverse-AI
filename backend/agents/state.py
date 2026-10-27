from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from agents.contracts import AgentResult


class AgentState(BaseModel):
    """Shared state passed through a FinVerse agent workflow."""

    model_config = ConfigDict(validate_assignment=True)

    request_id: UUID = Field(default_factory=uuid4)
    inputs: dict[str, Any] = Field(default_factory=dict)
    results: dict[str, AgentResult] = Field(default_factory=dict)
    decision_trace: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def record_result(self, result: AgentResult) -> None:
        """Store an agent result and append an auditable trace entry."""

        self.results[result.agent_name] = result

        self.decision_trace.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "agent_name": result.agent_name,
                "status": result.status.value,
                "error": result.error,
                "duration_ms": result.metadata.get("duration_ms"),
            }
        )
