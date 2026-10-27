from agents.contracts import AgentStatus
from agents.executor import AgentExecutor
from agents.registry import AgentRegistry


def test_executor_normalizes_successful_result():
    registry = AgentRegistry()
    registry.register("sample", lambda value: {"value": value})
    executor = AgentExecutor(registry)

    result = executor.execute("sample", value=42)

    assert result.status == AgentStatus.SUCCESS
    assert result.agent_name == "sample"
    assert result.data == {"value": 42}
    assert result.error is None
    assert result.metadata["duration_ms"] >= 0


def test_executor_wraps_non_dictionary_result():
    registry = AgentRegistry()
    registry.register("sample", lambda: 123)
    executor = AgentExecutor(registry)

    result = executor.execute("sample")

    assert result.status == AgentStatus.SUCCESS
    assert result.data == {"result": 123}


def test_executor_normalizes_agent_exception():
    def failing_agent():
        raise RuntimeError("Simulated failure")

    registry = AgentRegistry()
    registry.register("failing", failing_agent)
    executor = AgentExecutor(registry)

    result = executor.execute("failing")

    assert result.status == AgentStatus.FAILED
    assert result.error == "RuntimeError: Simulated failure"
    assert result.metadata["duration_ms"] >= 0


def test_executor_handles_unknown_agent():
    executor = AgentExecutor(AgentRegistry())

    result = executor.execute("unknown")

    assert result.status == AgentStatus.FAILED
    assert "not registered" in result.error


def test_executor_normalizes_pydantic_model_output():
    from pydantic import BaseModel

    class SampleOutput(BaseModel):
        score: int

    registry = AgentRegistry()
    registry.register("sample", lambda: SampleOutput(score=90))
    executor = AgentExecutor(registry)

    result = executor.execute("sample")

    assert result.status == AgentStatus.SUCCESS
    assert result.data == {"score": 90}
