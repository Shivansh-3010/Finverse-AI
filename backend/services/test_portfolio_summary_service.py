from decimal import Decimal
from unittest.mock import patch
from uuid import uuid4

from services.portfolio_summary_service import (
    PortfolioSummaryService,
)


def test_summary_combines_valuation_and_performance():
    portfolio_id = uuid4()

    valuation = {
        "positions": [
            {
                "symbol": "RELIANCE",
                "quantity": Decimal("2"),
                "market_value": Decimal("2200.00"),
            }
        ],
        "total_cost_basis": Decimal("2000.00"),
        "total_market_value": Decimal("2200.00"),
        "unrealized_pnl": Decimal("200.00"),
        "unrealized_return_pct": Decimal("10.00"),
    }

    performance = {
        "realized_pnl": Decimal("150.00"),
        "dividend_income": Decimal("25.00"),
        "total_realized_return": Decimal("175.00"),
        "total_bought": Decimal("2000.00"),
        "total_sold": Decimal("500.00"),
        "net_cash_flow": Decimal("-1475.00"),
    }

    beta = {"beta": Decimal("1.10")}
    risk_adjusted = {"risk_adjusted_return": Decimal("0.85")}

    with (
        patch(
            "services.portfolio_summary_service.portfolio_valuation_service.calculate",
            return_value=valuation,
        ),
        patch(
            "services.portfolio_summary_service.portfolio_performance_service.calculate",
            return_value=performance,
        ),
        patch(
            "services.portfolio_summary_service.portfolio_beta_service.calculate",
            return_value=beta,
        ),
        patch(
            "services.portfolio_summary_service.portfolio_risk_adjusted_service.calculate",
            return_value=risk_adjusted,
        ),
    ):
        result = PortfolioSummaryService.calculate(
            db=None,
            portfolio_id=portfolio_id,
        )

    assert result["portfolio_id"] == portfolio_id
    assert result["position_count"] == 1
    assert result["total_cost_basis"] == Decimal("2000.00")
    assert result["total_market_value"] == Decimal("2200.00")
    assert result["unrealized_pnl"] == Decimal("200.00")
    assert result["unrealized_return_pct"] == Decimal("10.00")
    assert result["realized_pnl"] == Decimal("150.00")
    assert result["dividend_income"] == Decimal("25.00")
    assert result["total_realized_return"] == Decimal("175.00")
    assert result["net_cash_flow"] == Decimal("-1475.00")
    assert result["beta"] == beta
    assert result["risk_adjusted"] == risk_adjusted