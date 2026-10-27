from agents.contracts import AgentStatus
from agents.orchestrator import AgentOrchestrator, AgentStep
from agents.registry import AgentRegistry
from agents.state import AgentState


def test_orchestrator_executes_steps_in_order():
    calls = []
    registry = AgentRegistry()

    def first(value):
        calls.append("first")
        return {"value": value}

    def second(value):
        calls.append("second")
        return {"value": value * 2}

    registry.register("first", first)
    registry.register("second", second)

    state = AgentState(inputs={"initial": 10})
    orchestrator = AgentOrchestrator(registry)

    result = orchestrator.run(
        state,
        [
            AgentStep(
                agent_name="first",
                input_mapping={"value": "initial"},
            ),
            AgentStep(
                agent_name="second",
                kwargs={"value": 5},
            ),
        ],
    )

    assert calls == ["first", "second"]
    assert result.results["first"].data == {"value": 10}
    assert result.results["second"].data == {"value": 10}
    assert len(result.decision_trace) == 2


def test_orchestrator_records_agent_failure_and_continues():
    registry = AgentRegistry()

    def failing_agent():
        raise RuntimeError("Simulated failure")

    registry.register("failing", failing_agent)
    registry.register("following", lambda: {"completed": True})

    state = AgentState()
    orchestrator = AgentOrchestrator(registry)

    result = orchestrator.run(
        state,
        [
            AgentStep(agent_name="failing"),
            AgentStep(agent_name="following"),
        ],
    )

    assert result.results["failing"].status == AgentStatus.FAILED
    assert result.results["following"].data == {"completed": True}
    assert len(result.decision_trace) == 2


def test_orchestrator_records_missing_input_as_failure():
    registry = AgentRegistry()
    registry.register("sample", lambda value: {"value": value})

    state = AgentState()
    orchestrator = AgentOrchestrator(registry)

    result = orchestrator.run(
        state,
        [
            AgentStep(
                agent_name="sample",
                input_mapping={"value": "missing"},
            ),
        ],
    )

    assert result.results["sample"].status == AgentStatus.FAILED
    assert "missing" in result.results["sample"].error
    assert len(result.decision_trace) == 1


def test_orchestrator_handles_unknown_agent():
    orchestrator = AgentOrchestrator(AgentRegistry())
    state = AgentState()

    result = orchestrator.run(
        state,
        [AgentStep(agent_name="unknown")],
    )

    assert result.results["unknown"].status == AgentStatus.FAILED
    assert "not registered" in result.results["unknown"].error


def test_parallel_execution_runs_independent_agents_concurrently():
    from threading import Barrier, current_thread

    barrier = Barrier(2)
    thread_names = []
    registry = AgentRegistry()

    def make_agent(name):
        def agent():
            thread_names.append((name, current_thread().name))
            barrier.wait(timeout=5)
            return {"agent": name}

        return agent

    registry.register("first", make_agent("first"))
    registry.register("second", make_agent("second"))

    state = AgentState()
    orchestrator = AgentOrchestrator(registry)

    result = orchestrator.run_parallel(
        state,
        [
            AgentStep(agent_name="first"),
            AgentStep(agent_name="second"),
        ],
        max_workers=2,
    )

    assert result.results["first"].data == {"agent": "first"}
    assert result.results["second"].data == {"agent": "second"}
    assert len(result.decision_trace) == 2
    assert [entry["agent_name"] for entry in result.decision_trace] == [
        "first",
        "second",
    ]
    assert all(name != thread for name, thread in thread_names)


def test_parallel_execution_isolates_agent_failure():
    registry = AgentRegistry()

    def failing_agent():
        raise RuntimeError("Parallel failure")

    registry.register("failing", failing_agent)
    registry.register("successful", lambda: {"ok": True})

    result = AgentOrchestrator(registry).run_parallel(
        AgentState(),
        [
            AgentStep(agent_name="failing"),
            AgentStep(agent_name="successful"),
        ],
        max_workers=2,
    )

    assert result.results["failing"].status == AgentStatus.FAILED
    assert result.results["successful"].data == {"ok": True}
    assert len(result.decision_trace) == 2


def test_parallel_execution_records_missing_inputs():
    registry = AgentRegistry()
    registry.register("sample", lambda value: {"value": value})

    result = AgentOrchestrator(registry).run_parallel(
        AgentState(),
        [
            AgentStep(
                agent_name="sample",
                input_mapping={"value": "missing"},
            ),
        ],
        max_workers=2,
    )

    assert result.results["sample"].status == AgentStatus.FAILED
    assert "missing" in result.results["sample"].error


def test_parallel_execution_rejects_invalid_worker_count():
    orchestrator = AgentOrchestrator(AgentRegistry())

    import pytest

    with pytest.raises(ValueError, match="max_workers"):
        orchestrator.run_parallel(
            AgentState(),
            [],
            max_workers=0,
        )


def test_conditional_router_executes_true_branch_only():
    registry = AgentRegistry()
    registry.register("true_agent", lambda: {"branch": "true"})
    registry.register("false_agent", lambda: {"branch": "false"})

    state = AgentState(inputs={"risk_score": 80})
    orchestrator = AgentOrchestrator(registry)

    result = orchestrator.run_conditional(
        state,
        condition=lambda current: current.inputs["risk_score"] >= 70,
        if_true=[AgentStep(agent_name="true_agent")],
        if_false=[AgentStep(agent_name="false_agent")],
    )

    assert "true_agent" in result.results
    assert "false_agent" not in result.results
    assert result.results["true_agent"].data == {"branch": "true"}


def test_conditional_router_executes_false_branch():
    registry = AgentRegistry()
    registry.register("true_agent", lambda: {"branch": "true"})
    registry.register("false_agent", lambda: {"branch": "false"})

    state = AgentState(inputs={"risk_score": 20})
    orchestrator = AgentOrchestrator(registry)

    result = orchestrator.run_conditional(
        state,
        condition=lambda current: current.inputs["risk_score"] >= 70,
        if_true=[AgentStep(agent_name="true_agent")],
        if_false=[AgentStep(agent_name="false_agent")],
    )

    assert "true_agent" not in result.results
    assert result.results["false_agent"].data == {"branch": "false"}


def test_conditional_router_records_condition_failure():
    registry = AgentRegistry()
    orchestrator = AgentOrchestrator(registry)
    state = AgentState()

    def invalid_condition(_state):
        raise RuntimeError("Condition failed")

    result = orchestrator.run_conditional(
        state,
        condition=invalid_condition,
        if_true=[],
    )

    assert result.results["conditional_router"].status == AgentStatus.FAILED
    assert "Condition failed" in result.results["conditional_router"].error
    assert len(result.decision_trace) == 1


def test_conditional_router_with_no_false_branch_runs_no_steps():
    registry = AgentRegistry()
    registry.register("true_agent", lambda: {"branch": "true"})

    state = AgentState()
    orchestrator = AgentOrchestrator(registry)

    result = orchestrator.run_conditional(
        state,
        condition=lambda _state: False,
        if_true=[AgentStep(agent_name="true_agent")],
    )

    assert result.results == {}
    assert result.decision_trace == []
