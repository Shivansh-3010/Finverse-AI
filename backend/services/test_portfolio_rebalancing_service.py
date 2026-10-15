from decimal import Decimal
from unittest.mock import patch
from uuid import uuid4

from services.portfolio_rebalancing_service import (
    PortfolioRebalancingService,
)


def _calculate(positions):
    portfolio_id = uuid4()

    optimization = {
        "positions": positions,
    }

    with patch(
        "services.portfolio_rebalancing_service."
        "portfolio_optimization_service.calculate",
        return_value=optimization,
    ):
        result = PortfolioRebalancingService.calculate(
            db=None,
            portfolio_id=portfolio_id,
        )

    return portfolio_id, result


def _position(symbol, current, target, change):
    return {
        "symbol": symbol,
        "current_weight_pct": Decimal(str(current)),
        "target_weight_pct": Decimal(str(target)),
        "weight_change_pct": Decimal(str(change)),
        "market_value": Decimal("1000"),
    }


def test_rebalancing_handles_empty_positions():
    portfolio_id, result = _calculate([])

    assert result["portfolio_id"] == portfolio_id
    assert result["position_count"] == 0
    assert result["estimated_turnover_pct"] is None
    assert result["rebalancing_required"] is False
    assert result["positions"] == []


def test_rebalancing_calculates_turnover_and_actions():
    positions = [
        _position("STOCK_A", "60", "45", "-15"),
        _position("STOCK_B", "25", "35", "10"),
        _position("STOCK_C", "15", "20", "5"),
    ]

    _, result = _calculate(positions)

    assert result["position_count"] == 3
    assert result["estimated_turnover_pct"] == Decimal("15.00")
    assert result["rebalancing_required"] is True

    by_symbol = {
        item["symbol"]: item
        for item in result["positions"]
    }

    assert by_symbol["STOCK_A"]["action"] == "REDUCE"
    assert by_symbol["STOCK_A"]["priority"] == "HIGH"

    assert by_symbol["STOCK_B"]["action"] == "INCREASE"
    assert by_symbol["STOCK_B"]["priority"] == "HIGH"

    assert by_symbol["STOCK_C"]["action"] == "INCREASE"
    assert by_symbol["STOCK_C"]["priority"] == "MEDIUM"


def test_rebalancing_holds_changes_below_one_percent():
    positions = [
        _position("STOCK_A", "50", "50.5", "0.5"),
        _position("STOCK_B", "50", "49.5", "-0.5"),
    ]

    _, result = _calculate(positions)

    assert result["estimated_turnover_pct"] == Decimal("0.50")
    assert result["rebalancing_required"] is False
    assert all(
        item["action"] == "HOLD"
        for item in result["positions"]
    )


def test_rebalancing_uses_one_percent_as_required_threshold():
    positions = [
        _position("STOCK_A", "51", "50", "-1"),
        _position("STOCK_B", "49", "50", "1"),
    ]

    _, result = _calculate(positions)

    assert result["estimated_turnover_pct"] == Decimal("1.00")
    assert result["rebalancing_required"] is True
    assert all(
        item["action"] != "HOLD"
        for item in result["positions"]
    )
