import pytest

from agents.contracts import AgentResult, AgentStatus
from agents.investment_committee import InvestmentCommittee
from agents.state import AgentState


def make_state(*results):
    state = AgentState()
    for result in results:
        state.record_result(result)
    return state


def test_bullish_consensus_recommends_buy():
    state = make_state(
        AgentResult(
            agent_name="technical",
            status=AgentStatus.SUCCESS,
            data={"signal": "bullish"},
        ),
        AgentResult(
            agent_name="news",
            status=AgentStatus.SUCCESS,
            data={"recommendation": "buy"},
        ),
    )

    decision = InvestmentCommittee().analyze(state)

    assert decision.recommendation == "BUY"
    assert decision.confidence == 1.0
    assert len(decision.supporting_evidence) == 2


def test_opposing_signals_produce_hold():
    state = make_state(
        AgentResult(
            agent_name="technical",
            status=AgentStatus.SUCCESS,
            data={"signal": "bullish"},
        ),
        AgentResult(
            agent_name="risk",
            status=AgentStatus.SUCCESS,
            data={"signal": "bearish"},
        ),
    )

    decision = InvestmentCommittee().analyze(state)

    assert decision.recommendation == "HOLD"
    assert decision.consensus == "conflicted"


def test_failed_agents_are_reported():
    state = make_state(
        AgentResult(
            agent_name="technical",
            status=AgentStatus.SUCCESS,
            data={"signal": "bullish"},
        ),
        AgentResult(
            agent_name="news",
            status=AgentStatus.FAILED,
            error="Source unavailable",
        ),
    )

    decision = InvestmentCommittee().analyze(state)

    assert decision.recommendation == "BUY"
    assert decision.failed_agents == ["news"]
    assert "incomplete" in decision.rationale


def test_no_recognized_signals_returns_insufficient_data():
    state = make_state(
        AgentResult(
            agent_name="technical",
            status=AgentStatus.SUCCESS,
            data={"candlestick_score": 5},
        )
    )

    decision = InvestmentCommittee().analyze(state)

    assert decision.recommendation == "INSUFFICIENT_DATA"
    assert decision.confidence == 0.0


def test_neutral_signals_recommend_hold():
    state = make_state(
        AgentResult(
            agent_name="technical",
            status=AgentStatus.SUCCESS,
            data={"signal": "neutral"},
        )
    )

    decision = InvestmentCommittee().analyze(state)

    assert decision.recommendation == "HOLD"
    assert decision.consensus == "neutral"


def test_agent_with_internal_conflicting_signals_is_not_directional_vote():
    state = make_state(
        AgentResult(
            agent_name="technical",
            status=AgentStatus.SUCCESS,
            data={"signal": "bullish", "trend_signal": "bearish"},
        ),
        AgentResult(
            agent_name="news",
            status=AgentStatus.SUCCESS,
            data={"signal": "bullish"},
        ),
    )

    decision = InvestmentCommittee().analyze(state)

    assert decision.recommendation == "BUY"
    assert len(decision.conflicting_evidence) == 2
    assert decision.confidence == 0.5
