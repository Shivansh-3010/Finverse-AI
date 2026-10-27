from agents.contracts import AgentResult, AgentStatus
from agents.failure_policy import FailureMode, FailurePolicy


def test_continue_mode_continues_after_failure():
    policy = FailurePolicy(mode=FailureMode.CONTINUE)
    result = AgentResult(
        agent_name="news",
        status=AgentStatus.FAILED,
        error="Source unavailable",
    )

    assert policy.should_continue(result) is True


def test_stop_mode_stops_after_failure():
    policy = FailurePolicy(mode=FailureMode.STOP)
    result = AgentResult(
        agent_name="news",
        status=AgentStatus.FAILED,
        error="Source unavailable",
    )

    assert policy.should_continue(result) is False


def test_require_success_stops_when_required_agent_fails():
    policy = FailurePolicy(
        mode=FailureMode.REQUIRE_SUCCESS,
        required_agents={"risk"},
    )
    result = AgentResult(
        agent_name="risk",
        status=AgentStatus.FAILED,
        error="Risk analysis failed",
    )

    assert policy.should_continue(result) is False


def test_require_success_allows_optional_agent_failure():
    policy = FailurePolicy(
        mode=FailureMode.REQUIRE_SUCCESS,
        required_agents={"risk"},
    )
    result = AgentResult(
        agent_name="news",
        status=AgentStatus.FAILED,
        error="News unavailable",
    )

    assert policy.should_continue(result) is True


def test_partial_required_result_can_be_rejected():
    policy = FailurePolicy(
        required_agents={"risk"},
        allow_partial_results=False,
    )
    result = AgentResult(
        agent_name="risk",
        status=AgentStatus.PARTIAL,
    )

    assert policy.should_continue(result) is False


def test_required_result_validation_reports_missing_and_failed_agents():
    policy = FailurePolicy(required_agents={"risk", "news"})
    results = {
        "risk": AgentResult(
            agent_name="risk",
            status=AgentStatus.SUCCESS,
        ),
        "news": AgentResult(
            agent_name="news",
            status=AgentStatus.FAILED,
            error="Unavailable",
        ),
    }

    valid, missing = policy.validate_required_results(results)

    assert valid is False
    assert missing == ["news"]
