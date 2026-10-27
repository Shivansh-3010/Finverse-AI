from agents.contracts import AgentResult, AgentStatus
from agents.state import AgentState


def test_state_generates_unique_request_ids():
    first = AgentState()
    second = AgentState()

    assert first.request_id != second.request_id


def test_state_starts_with_empty_collections():
    state = AgentState()

    assert state.inputs == {}
    assert state.results == {}
    assert state.decision_trace == []



def test_record_result_updates_results_and_decision_trace():
    state = AgentState()
    result = AgentResult(
        agent_name="technical_analysis",
        status=AgentStatus.SUCCESS,
        data={"technical_score": 82},
        metadata={"duration_ms": 12.5},
    )

    state.record_result(result)

    assert state.results["technical_analysis"] == result
    assert len(state.decision_trace) == 1

    trace = state.decision_trace[0]
    assert trace["agent_name"] == "technical_analysis"
    assert trace["status"] == "success"
    assert trace["error"] is None
    assert trace["duration_ms"] == 12.5
    assert "timestamp" in trace


def test_record_result_tracks_failed_agent():
    state = AgentState()
    result = AgentResult(
        agent_name="prediction",
        status=AgentStatus.FAILED,
        error="Model unavailable",
    )

    state.record_result(result)

    assert state.results["prediction"].status == AgentStatus.FAILED
    assert state.decision_trace[0]["error"] == "Model unavailable"


def test_recording_multiple_results_preserves_trace_order():
    state = AgentState()

    for name in ("technical_analysis", "risk_analysis"):
        state.record_result(
            AgentResult(
                agent_name=name,
                status=AgentStatus.SUCCESS,
            )
        )

    assert [
        entry["agent_name"] for entry in state.decision_trace
    ] == ["technical_analysis", "risk_analysis"]
    assert len(state.results) == 2
