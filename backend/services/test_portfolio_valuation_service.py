from decimal import Decimal
from unittest.mock import MagicMock, patch
from uuid import uuid4

from services.portfolio_valuation_service import (
    PortfolioValuationService,
)


def test_valuation_calculates_market_value_and_unrealized_pnl():
    portfolio_id = uuid4()

    holdings = [
        {
            "symbol": "RELIANCE",
            "quantity": Decimal("2"),
            "avg_price": Decimal("1000.00"),
            "cost_basis": Decimal("2000.00"),
        }
    ]

    candle = MagicMock()
    candle.close = Decimal("1100.00")

    performance = {
        "cash_balance": Decimal("500.00"),
    }

    with (
        patch(
            "services.portfolio_valuation_service.holding_service.calculate_from_transactions",
            return_value=holdings,
        ),
        patch(
            "services.portfolio_valuation_service.portfolio_performance_service.calculate",
            return_value=performance,
        ),
        patch(
            "services.portfolio_valuation_service.OHLCVRepository",
        ) as repository_class,
    ):
        repository_class.return_value.get_latest_candle.return_value = candle

        result = PortfolioValuationService.calculate(
            db=MagicMock(),
            portfolio_id=portfolio_id,
        )

    assert result["total_cost_basis"] == Decimal("2000.00")
    assert result["total_market_value"] == Decimal("2200.00")
    assert result["cash_balance"] == Decimal("500.00")
    assert result["total_portfolio_value"] == Decimal("2700.00")
    assert result["unrealized_pnl"] == Decimal("200.00")
    assert result["unrealized_return_pct"] == Decimal("10.00")
    assert result["positions"][0]["market_value"] == Decimal("2200.00")
    assert result["positions"][0]["portfolio_weight_pct"] == Decimal("100.00")
    assert result["valuation_complete"] is True
    assert result["unpriced_positions"] == []


def test_valuation_handles_missing_market_price():
    portfolio_id = uuid4()

    holdings = [
        {
            "symbol": "RELIANCE",
            "quantity": Decimal("2"),
            "avg_price": Decimal("1000.00"),
            "cost_basis": Decimal("2000.00"),
        }
    ]

    performance = {
        "cash_balance": Decimal("500.00"),
    }

    with (
        patch(
            "services.portfolio_valuation_service.holding_service.calculate_from_transactions",
            return_value=holdings,
        ),
        patch(
            "services.portfolio_valuation_service.portfolio_performance_service.calculate",
            return_value=performance,
        ),
        patch(
            "services.portfolio_valuation_service.OHLCVRepository",
        ) as repository_class,
    ):
        repository_class.return_value.get_latest_candle.return_value = None

        result = PortfolioValuationService.calculate(
            db=MagicMock(),
            portfolio_id=portfolio_id,
        )

    assert result["positions"] == []
    assert result["total_cost_basis"] == Decimal("0.00")
    assert result["total_market_value"] == Decimal("0.00")
    assert result["cash_balance"] == Decimal("500.00")
    assert result["total_portfolio_value"] == Decimal("500.00")
    assert result["unrealized_pnl"] == Decimal("0.00")
    assert result["unrealized_return_pct"] == Decimal("0.00")

    assert result["valuation_complete"] is False
    assert result["unpriced_positions"] == ["RELIANCE"]