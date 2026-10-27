from time import perf_counter
from typing import Any

from agents.contracts import AgentResult, AgentStatus
from agents.registry import AgentRegistry


class AgentExecutor:
    """Execute registered agents and normalize their results."""

    def __init__(self, registry: AgentRegistry) -> None:
        self.registry = registry

    def execute(
        self,
        agent_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> AgentResult:
        started_at = perf_counter()

        try:
            agent = self.registry.get(agent_name)
            output = agent(*args, **kwargs)

            if isinstance(output, dict):
                data = output
            elif hasattr(output, "model_dump") and callable(output.model_dump):
                data = output.model_dump()
            else:
                data = {"result": output}

            return AgentResult(
                agent_name=agent_name,
                status=AgentStatus.SUCCESS,
                data=data,
                metadata={
                    "duration_ms": round(
                        (perf_counter() - started_at) * 1000,
                        2,
                    )
                },
            )

        except Exception as exc:
            return AgentResult(
                agent_name=agent_name,
                status=AgentStatus.FAILED,
                error=f"{type(exc).__name__}: {exc}",
                metadata={
                    "duration_ms": round(
                        (perf_counter() - started_at) * 1000,
                        2,
                    )
                },
            )
