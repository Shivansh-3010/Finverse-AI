from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from agents.contracts import AgentResult, AgentStatus
from agents.executor import AgentExecutor
from agents.registry import AgentRegistry
from agents.state import AgentState


class AgentStep(BaseModel):
    """Explicit configuration for one sequential agent invocation."""

    model_config = ConfigDict(extra="forbid")

    agent_name: str = Field(min_length=1)
    input_mapping: dict[str, str] = Field(default_factory=dict)
    kwargs: dict[str, Any] = Field(default_factory=dict)


class AgentOrchestrator:
    """Run configured agents sequentially using shared workflow state."""

    def __init__(self, registry: AgentRegistry) -> None:
        self.registry = registry
        self.executor = AgentExecutor(registry)

    def run(
        self,
        state: AgentState,
        steps: list[AgentStep],
    ) -> AgentState:
        for step in steps:
            kwargs = dict(step.kwargs)

            try:
                for argument_name, state_key in step.input_mapping.items():
                    if state_key not in state.inputs:
                        raise KeyError(
                            f"Input '{state_key}' required by agent "
                            f"'{step.agent_name}' is missing."
                        )

                    kwargs[argument_name] = state.inputs[state_key]

                result = self.executor.execute(
                    step.agent_name,
                    **kwargs,
                )

            except Exception as exc:
                result = AgentResult(
                    agent_name=step.agent_name,
                    status=AgentStatus.FAILED,
                    error=f"{type(exc).__name__}: {exc}",
                )

            state.record_result(result)

        return state

    def run_parallel(
        self,
        state: AgentState,
        steps: list[AgentStep],
        max_workers: int | None = None,
    ) -> AgentState:
        """Execute independent steps concurrently and record results in step order."""

        from concurrent.futures import ThreadPoolExecutor

        if max_workers is not None and max_workers < 1:
            raise ValueError("max_workers must be at least 1.")

        prepared_steps = []
        results_by_index = {}

        for index, step in enumerate(steps):
            kwargs = dict(step.kwargs)

            try:
                for argument_name, state_key in step.input_mapping.items():
                    if state_key not in state.inputs:
                        raise KeyError(
                            f"Input '{state_key}' required by agent "
                            f"'{step.agent_name}' is missing."
                        )

                    kwargs[argument_name] = state.inputs[state_key]

                prepared_steps.append((index, step, kwargs))

            except Exception as exc:
                results_by_index[index] = AgentResult(
                    agent_name=step.agent_name,
                    status=AgentStatus.FAILED,
                    error=f"{type(exc).__name__}: {exc}",
                )

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {
                index: pool.submit(
                    self.executor.execute,
                    step.agent_name,
                    **kwargs,
                )
                for index, step, kwargs in prepared_steps
            }

            for index, future in futures.items():
                try:
                    results_by_index[index] = future.result()
                except Exception as exc:
                    step = steps[index]
                    results_by_index[index] = AgentResult(
                        agent_name=step.agent_name,
                        status=AgentStatus.FAILED,
                        error=f"{type(exc).__name__}: {exc}",
                    )

        for index in range(len(steps)):
            state.record_result(results_by_index[index])

        return state

    def run_conditional(
        self,
        state: AgentState,
        condition,
        if_true: list[AgentStep],
        if_false: list[AgentStep] | None = None,
    ) -> AgentState:
        """Execute one workflow branch based on shared state."""

        try:
            branch_steps = if_true if condition(state) else (if_false or [])
        except Exception as exc:
            result = AgentResult(
                agent_name="conditional_router",
                status=AgentStatus.FAILED,
                error=f"{type(exc).__name__}: {exc}",
            )
            state.record_result(result)
            return state

        return self.run(state, branch_steps)

    def run_investment_committee(
        self,
        state: AgentState,
        steps: list[AgentStep],
        parallel: bool = False,
        max_workers: int | None = None,
    ):
        """Run agent analyses and return their shared state with a committee decision."""
        from agents.investment_committee import InvestmentCommittee

        if parallel:
            self.run_parallel(state, steps, max_workers=max_workers)
        else:
            self.run(state, steps)

        decision = InvestmentCommittee().analyze(state)
        state.metadata["investment_committee"] = decision.model_dump()
        state.decision_trace.append({
            "agent_name": "investment_committee",
            "status": "success",
            "recommendation": decision.recommendation,
            "confidence": decision.confidence,
            "consensus": decision.consensus,
            "failed_agents": decision.failed_agents,
        })
        return state, decision