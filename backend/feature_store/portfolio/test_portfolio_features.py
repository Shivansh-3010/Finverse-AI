
from feature_store.portfolio.portfolio_features import (
    generate_portfolio_features,
)


def test_extracts_existing_portfolio_analytics():
    intelligence = {
        "portfolio_id": "portfolio-123",
        "benchmark": "NIFTY50",
        "timeframe": "1d",
        "lookback_days": 30,
        "intelligence_category": "Moderate Risk",
        "overall_risk_score": 45,
        "risk_category": "Moderate",
        "portfolio_summary": {
            "position_count": 4,
            "total_market_value": 100000,
            "herfindahl_index": 3200,
            "largest_position": {
                "portfolio_weight_pct": 40,
            },
        },
        "risk": {
            "drawdown": {"maximum_drawdown_pct": -12.5},
            "var": {"var_95_pct": 3.2},
        },
        "portfolio_structure": {
            "diversification": {
                "diversification_score": 68,
                "effective_number_of_positions": 3.1,
                "concentration_score": 32,
                "average_pairwise_correlation": 0.45,
            },
            "liquidity": {"portfolio_liquidity_score": 82},
        },
        "risk_flags": ["High concentration"],
    }

    result = generate_portfolio_features(intelligence)
    features = result["features"]

    assert result["portfolio_id"] == "portfolio-123"
    assert result["source"] == "portfolio_intelligence_service"
    assert result["feature_count"] == 12
    assert result["available_feature_count"] == 12
    assert features["position_count"] == 4
    assert features["largest_position_weight_pct"] == 40
    assert features["maximum_drawdown_pct"] == -12.5
    assert features["var_95_pct"] == 3.2
    assert features["liquidity_score"] == 82
    assert result["risk_flags"] == ["High concentration"]


def test_missing_analytics_remain_none():
    result = generate_portfolio_features({
        "portfolio_id": "portfolio-empty",
        "portfolio_summary": {},
        "risk": {},
        "portfolio_structure": {},
    })

    assert result["available_feature_count"] == 0
    assert all(
        value is None
        for value in result["features"].values()
    )


def test_invalid_numeric_values_are_not_exposed():
    result = generate_portfolio_features({
        "portfolio_summary": {
            "position_count": "invalid",
            "total_market_value": float("inf"),
        },
        "risk": {},
        "portfolio_structure": {},
    })

    assert result["features"]["position_count"] is None
    assert result["features"]["total_market_value"] is None
