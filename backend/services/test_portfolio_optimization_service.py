from decimal import Decimal
from unittest.mock import patch
from uuid import uuid4

from services.portfolio_optimization_service import (
    PortfolioOptimizationService,
)


def _exposure(positions, total_market_value):
    return {
        "exposures": positions,
        "total_market_value": Decimal(str(total_market_value)),
    }


def _position(symbol, weight, market_value):
    return {
        "symbol": symbol,
        "portfolio_weight_pct": Decimal(str(weight)),
        "market_value": Decimal(str(market_value)),
    }


def _calculate(portfolio_id, exposure):
    with (
        patch(
            "services.portfolio_optimization_service."
            "portfolio_exposure_service.calculate",
            return_value=exposure,
        ),
        patch(
            "services.portfolio_optimization_service."
            "portfolio_risk_score_service.calculate",
            return_value={"overall_risk_score": Decimal("45")},
        ),
    ):
        return PortfolioOptimizationService.calculate(
            db=None,
            portfolio_id=portfolio_id,
        )


def test_optimization_handles_empty_portfolio():
    portfolio_id = uuid4()

    result = _calculate(
        portfolio_id,
        _exposure([], "0"),
    )

    assert result["portfolio_id"] == portfolio_id
    assert result["position_count"] == 0
    assert result["optimization_category"] == "Insufficient Data"
    assert result["positions"] == []
    assert result["current_concentration_score"] is None
    assert result["optimized_concentration_score"] is None
    assert result["expected_risk_reduction_pct"] is None


def test_optimization_calculates_concentration_and_targets():
    portfolio_id = uuid4()
    exposure = _exposure(
        [
            _position("STOCK_A", "60", "6000"),
            _position("STOCK_B", "25", "2500"),
            _position("STOCK_C", "15", "1500"),
        ],
        "10000",
    )

    result = _calculate(portfolio_id, exposure)

    assert result["position_count"] == 3
    assert result["current_concentration_score"] == Decimal("4450.00")
    assert result["optimized_concentration_score"] < result[
        "current_concentration_score"
    ]
    assert result["expected_risk_reduction_pct"] > Decimal("0")

    targets = {
        position["symbol"]: position["target_weight_pct"]
        for position in result["positions"]
    }

    # Three positions can satisfy the 40% maximum allocation.
    assert all(weight <= Decimal("40.00") for weight in targets.values())

    # Allow for rounding each target to two decimal places.
    assert abs(
        sum(targets.values(), Decimal("0")) - Decimal("100")
    ) <= Decimal("0.02")


def test_optimization_handles_two_positions_without_losing_allocation():
    portfolio_id = uuid4()
    exposure = _exposure(
        [
            _position("STOCK_A", "70", "7000"),
            _position("STOCK_B", "30", "3000"),
        ],
        "10000",
    )

    result = _calculate(portfolio_id, exposure)

    targets = [
        position["target_weight_pct"]
        for position in result["positions"]
    ]

    # A strict 40% cap is mathematically impossible with two positions.
    assert all(weight <= Decimal("50.00") for weight in targets)
    assert abs(
        sum(targets, Decimal("0")) - Decimal("100")
    ) <= Decimal("0.02")