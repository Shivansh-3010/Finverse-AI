from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import Mock, patch
from uuid import uuid4
import pytest

from services.portfolio_xirr_service import (
    PortfolioXIRRService,
    _xirr,
)


def test_xirr_simple_annual_return():
    start = datetime(
        2025,
        1,
        1,
        tzinfo=timezone.utc,
    )

    end = datetime(
        2026,
        1,
        1,
        tzinfo=timezone.utc,
    )

    cash_flows = [
        (start, Decimal("-1000")),
        (end, Decimal("1100")),
    ]

    result = _xirr(cash_flows)

    assert result > Decimal("0.09")
    assert result < Decimal("0.11")


def test_xirr_requires_positive_and_negative_cash_flow():
    start = datetime(
        2025,
        1,
        1,
        tzinfo=timezone.utc,
    )

    end = datetime(
        2026,
        1,
        1,
        tzinfo=timezone.utc,
    )

    cash_flows = [
        (start, Decimal("-1000")),
        (end, Decimal("-1100")),
    ]

    result = _xirr(cash_flows)

    assert result == Decimal("0")


def test_xirr_requires_at_least_two_cash_flows():
    start = datetime(
        2025,
        1,
        1,
        tzinfo=timezone.utc,
    )

    cash_flows = [
        (start, Decimal("-1000")),
    ]

    result = _xirr(cash_flows)

    assert result == Decimal("0")
    
def test_xirr_rejects_incomplete_portfolio_valuation():
    portfolio_id = uuid4()

    with (
        patch(
            "services.portfolio_xirr_service.portfolio_transaction_repository.get_by_portfolio",
            return_value=[],
        ),
        patch(
            "services.portfolio_xirr_service.portfolio_valuation_service.calculate",
            return_value={
                "total_portfolio_value": Decimal("500.00"),
                "valuation_complete": False,
                "unpriced_positions": ["RELIANCE"],
            },
        ),
    ):
        with pytest.raises(
            ValueError,
            match="valuation is incomplete",
        ):
            PortfolioXIRRService.calculate(
                db=Mock(),
                portfolio_id=portfolio_id,
            )