
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any
from uuid import UUID


def _number(value: Any) -> float | None:
    """Convert a numeric value to a finite float; preserve missing data."""
    if value is None:
        return None

    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        return None

    if number != number or number in (float("inf"), float("-inf")):
        return None

    return number


def generate_portfolio_features(
    intelligence: dict[str, Any],
) -> dict[str, Any]:
    """
    Normalize existing portfolio intelligence into ML-friendly features.

    This function performs no database queries and does not recalculate
    portfolio analytics. Missing upstream values remain None.
    """
    summary = intelligence.get("portfolio_summary") or {}
    risk = intelligence.get("risk") or {}
    structure = intelligence.get("portfolio_structure") or {}

    risk_score = risk.get("risk_score") or {}
    drawdown = risk.get("drawdown") or {}
    var = risk.get("var") or {}
    diversification = structure.get("diversification") or {}
    liquidity = structure.get("liquidity") or {}
    factor_exposure = structure.get("factor_exposure") or {}
    largest_position = summary.get("largest_position") or {}

    exposure_weight = _number(
        largest_position.get("portfolio_weight_pct")
    )

    features = {
        "position_count": _number(summary.get("position_count")),
        "total_market_value": _number(summary.get("total_market_value")),
        "herfindahl_index": _number(summary.get("herfindahl_index")),
        "largest_position_weight_pct": exposure_weight,
        "overall_risk_score": _number(
            intelligence.get("overall_risk_score")
        ),
        "maximum_drawdown_pct": _number(
            drawdown.get("maximum_drawdown_pct")
        ),
        "var_95_pct": _number(
            var.get("var_95_pct")
        ),
        "diversification_score": _number(
            diversification.get("diversification_score")
        ),
        "effective_number_of_positions": _number(
            diversification.get("effective_number_of_positions")
        ),
        "concentration_score": _number(
            diversification.get("concentration_score")
        ),
        "average_pairwise_correlation": _number(
            diversification.get("average_pairwise_correlation")
        ),
        "liquidity_score": _number(
            liquidity.get("portfolio_liquidity_score")
        ),
    }

    return {
        "portfolio_id": str(intelligence.get("portfolio_id", "")),
        "benchmark": intelligence.get("benchmark"),
        "timeframe": intelligence.get("timeframe"),
        "lookback_days": intelligence.get("lookback_days"),
        "intelligence_category": intelligence.get(
            "intelligence_category"
        ),
        "risk_category": intelligence.get("risk_category"),
        "risk_flags": list(intelligence.get("risk_flags") or []),
        "features": features,
        "feature_count": len(features),
        "available_feature_count": sum(
            value is not None for value in features.values()
        ),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "portfolio_intelligence_service",
    }
