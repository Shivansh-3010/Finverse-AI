
from uuid import uuid4
from unittest.mock import patch

from services.copilot_service import CopilotService


def test_analyze_portfolio_returns_intelligence_and_recommendations():
    portfolio_id = uuid4()
    db = object()

    intelligence = {
        "portfolio_id": str(portfolio_id),
        "benchmark": "NIFTY50",
        "timeframe": "1d",
        "lookback_days": 30,
        "intelligence_category": "moderate",
        "overall_risk_score": 42,
        "risk_category": "MODERATE",
        "portfolio_summary": {"position_count": 5},
        "risk_flags": ["High concentration"],
    }

    recommendation_result = {
        "recommendations": [
            {
                "action": "REVIEW_CONCENTRATION",
                "priority": "HIGH",
                "reason": "Largest position exceeds the desired threshold.",
            },
            {
                "action": "REVIEW_DIVERSIFICATION",
                "priority": "MEDIUM",
                "reason": "Portfolio diversification could be improved.",
            },
        ]
    }

    with (
        patch(
            "services.copilot_service.portfolio_intelligence_service.calculate",
            return_value=intelligence,
        ) as intelligence_mock,
        patch(
            "services.copilot_service.portfolio_recommendation_service.calculate",
            return_value=recommendation_result,
        ) as recommendation_mock,
        patch(
            "services.copilot_service.MonitoringMetrics.increment_copilot_requests"
        ) as metrics_mock,
    ):
        result = CopilotService.analyze_portfolio(
            db=db,
            portfolio_id=portfolio_id,
        )

    assert result["portfolio_id"] == str(portfolio_id)
    assert result["intelligence_category"] == "moderate"
    assert result["overall_risk_score"] == 42
    assert result["risk_flags"] == ["High concentration"]
    assert result["recommendations"] == recommendation_result["recommendations"]
    assert result["recommendation_count"] == 2
    assert "not a guarantee" in result["message"]

    intelligence_mock.assert_called_once_with(
        db=db,
        portfolio_id=portfolio_id,
        benchmark="NIFTY50",
        timeframe="1d",
        lookback_days=30,
    )
    recommendation_mock.assert_called_once_with(
        db=db,
        portfolio_id=portfolio_id,
        benchmark="NIFTY50",
        timeframe="1d",
        lookback_days=30,
    )
    metrics_mock.assert_called_once()


def test_analyze_portfolio_handles_missing_risk_score():
    portfolio_id = uuid4()

    intelligence = {
        "intelligence_category": "unknown",
        "overall_risk_score": None,
        "portfolio_summary": {},
        "risk_flags": [],
    }

    with (
        patch(
            "services.copilot_service.portfolio_intelligence_service.calculate",
            return_value=intelligence,
        ),
        patch(
            "services.copilot_service.portfolio_recommendation_service.calculate",
            return_value={"recommendations": []},
        ),
        patch(
            "services.copilot_service.MonitoringMetrics.increment_copilot_requests"
        ),
    ):
        result = CopilotService.analyze_portfolio(
            db=object(),
            portfolio_id=portfolio_id,
        )

    assert result["overall_risk_score"] is None
    assert result["recommendation_count"] == 0
    assert "insufficient risk-score data" in result["summary"]
