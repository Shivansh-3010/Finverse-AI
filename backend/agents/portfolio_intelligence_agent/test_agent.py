
from uuid import uuid4
from unittest.mock import patch

from agents.portfolio_intelligence_agent.agent import (
    PortfolioIntelligenceAgent,
)


def test_agent_returns_structured_portfolio_intelligence():
    portfolio_id = uuid4()
    db = object()

    intelligence = {
        "intelligence_category": "moderate",
        "overall_risk_score": 42,
        "risk_category": "MODERATE",
        "portfolio_summary": {"position_count": 5},
        "risk": {"drawdown": {"maximum_drawdown_pct": 12.5}},
        "portfolio_structure": {"diversification": {}},
        "risk_flags": ["High concentration"],
        "message": None,
        "internal_field": "not exposed",
    }

    agent = PortfolioIntelligenceAgent()

    with patch(
        "agents.portfolio_intelligence_agent.agent."
        "portfolio_intelligence_service.calculate",
        return_value=intelligence,
    ) as calculate_mock:
        result = agent.analyze(
            db=db,
            portfolio_id=portfolio_id,
        )

    assert result["portfolio_id"] == str(portfolio_id)
    assert result["intelligence_category"] == "moderate"
    assert result["overall_risk_score"] == 42
    assert result["risk_flags"] == ["High concentration"]
    assert result["portfolio_summary"] == {"position_count": 5}
    assert "internal_field" not in result

    calculate_mock.assert_called_once_with(
        db=db,
        portfolio_id=portfolio_id,
        benchmark="NIFTY50",
        timeframe="1d",
        lookback_days=30,
    )


def test_agent_handles_missing_optional_sections():
    portfolio_id = uuid4()
    agent = PortfolioIntelligenceAgent()

    with patch(
        "agents.portfolio_intelligence_agent.agent."
        "portfolio_intelligence_service.calculate",
        return_value={},
    ):
        result = agent.analyze(
            db=object(),
            portfolio_id=portfolio_id,
        )

    assert result["portfolio_id"] == str(portfolio_id)
    assert result["portfolio_summary"] == {}
    assert result["risk"] == {}
    assert result["portfolio_structure"] == {}
    assert result["risk_flags"] == []
