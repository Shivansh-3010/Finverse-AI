from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from agents.contracts import AgentResult, AgentStatus


class FailureMode(StrEnum):
    CONTINUE = "continue"
    STOP = "stop"
    REQUIRE_SUCCESS = "require_success"


class FailurePolicy(BaseModel):
    """Configurable policy for handling agent execution outcomes."""

    model_config = ConfigDict(extra="forbid")

    mode: FailureMode = FailureMode.CONTINUE
    required_agents: set[str] = Field(default_factory=set)
    allow_partial_results: bool = True

    def should_continue(self, result: AgentResult) -> bool:
        if result.status == AgentStatus.FAILED:
            if self.mode == FailureMode.STOP:
                return False
            if (
                self.mode == FailureMode.REQUIRE_SUCCESS
                and result.agent_name in self.required_agents
            ):
                return False

        if (
            result.status == AgentStatus.PARTIAL
            and not self.allow_partial_results
            and result.agent_name in self.required_agents
        ):
            return False

        return True

    def validate_required_results(
        self,
        results: dict[str, AgentResult],
    ) -> tuple[bool, list[str]]:
        missing = sorted(
            name
            for name in self.required_agents
            if name not in results
            or results[name].status != AgentStatus.SUCCESS
        )
        return not missing, missing
