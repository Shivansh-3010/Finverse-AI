import pytest
from pydantic import ValidationError

from agents.contracts import AgentResult, AgentStatus


def test_agent_result_accepts_successful_result():
    result = AgentResult(
        agent_name="technical_analysis",
        status=AgentStatus.SUCCESS,
        data={"technical_score": 82},
    )

    assert result.agent_name == "technical_analysis"
    assert result.status == AgentStatus.SUCCESS
    assert result.data == {"technical_score": 82}
    assert result.error is None
    assert result.warnings == []
    assert result.metadata == {}


def test_agent_result_accepts_failure_details():
    result = AgentResult(
        agent_name="prediction",
        status=AgentStatus.FAILED,
        error="Model unavailable",
    )

    assert result.status == AgentStatus.FAILED
    assert result.error == "Model unavailable"
    assert result.data == {}


def test_agent_result_rejects_empty_agent_name():
    with pytest.raises(ValidationError):
        AgentResult(
            agent_name="",
            status=AgentStatus.SUCCESS,
        )


def test_agent_result_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        AgentResult(
            agent_name="technical_analysis",
            status=AgentStatus.SUCCESS,
            unexpected_field=True,
        )


@pytest.mark.parametrize(
    "status",
    [
        AgentStatus.SUCCESS,
        AgentStatus.PARTIAL,
        AgentStatus.SKIPPED,
        AgentStatus.FAILED,
    ],
)
def test_agent_result_supports_all_statuses(status):
    result = AgentResult(
        agent_name="test_agent",
        status=status,
    )

    assert result.status == status
