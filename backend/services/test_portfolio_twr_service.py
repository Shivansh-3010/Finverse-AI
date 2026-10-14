from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import patch
from uuid import uuid4

from services.portfolio_twr_service import PortfolioTWRService


def test_twr_requires_at_least_two_snapshots():
    portfolio_id = uuid4()

    snapshot = type(
        "Snapshot",
        (),
        {
            "portfolio_value": Decimal("1000"),
            "snapshot_time": datetime(
                2026,
                1,
                1,
                tzinfo=timezone.utc,
            ),
        },
    )()

    with patch(
        "services.portfolio_twr_service.portfolio_snapshot_repository.get_by_portfolio",
        return_value=[snapshot],
    ):
        result = PortfolioTWRService.calculate(
            db=None,
            portfolio_id=portfolio_id,
        )

    assert result["snapshot_count"] == 1
    assert result["period_count"] == 0
    assert result["twr"] == Decimal("0.00")
    assert result["twr_pct"] == Decimal("0.00")
    assert result["periods"] == []


def test_twr_calculates_simple_return_without_cash_flow():
    portfolio_id = uuid4()

    snapshots = [
        type(
            "Snapshot",
            (),
            {
                "portfolio_value": Decimal("1000"),
                "snapshot_time": datetime(
                    2026,
                    1,
                    1,
                    tzinfo=timezone.utc,
                ),
            },
        )(),
        type(
            "Snapshot",
            (),
            {
                "portfolio_value": Decimal("1100"),
                "snapshot_time": datetime(
                    2026,
                    2,
                    1,
                    tzinfo=timezone.utc,
                ),
            },
        )(),
    ]

    with patch(
        "services.portfolio_twr_service.portfolio_snapshot_repository.get_by_portfolio",
        return_value=snapshots,
    ), patch(
        "services.portfolio_twr_service.portfolio_transaction_repository.get_by_portfolio",
        return_value=[],
    ):
        result = PortfolioTWRService.calculate(
            db=None,
            portfolio_id=portfolio_id,
        )

    assert result["snapshot_count"] == 2
    assert result["period_count"] == 1
    assert result["twr"] == Decimal("10.00")
    assert result["twr_pct"] == Decimal("10.00")
    assert result["periods"][0]["return"] == Decimal("10.00")


def test_twr_adjusts_for_external_deposit():
    portfolio_id = uuid4()

    snapshots = [
        type(
            "Snapshot",
            (),
            {
                "portfolio_value": Decimal("1000"),
                "snapshot_time": datetime(
                    2026,
                    1,
                    1,
                    tzinfo=timezone.utc,
                ),
            },
        )(),
        type(
            "Snapshot",
            (),
            {
                "portfolio_value": Decimal("2200"),
                "snapshot_time": datetime(
                    2026,
                    2,
                    1,
                    tzinfo=timezone.utc,
                ),
            },
        )(),
    ]

    deposit = type(
        "Transaction",
        (),
        {
            "transaction_type": "DEPOSIT",
            "amount": Decimal("1000"),
            "transaction_date": datetime(
                2026,
                1,
                15,
                tzinfo=timezone.utc,
            ),
        },
    )()

    with patch(
        "services.portfolio_twr_service.portfolio_snapshot_repository.get_by_portfolio",
        return_value=snapshots,
    ), patch(
        "services.portfolio_twr_service.portfolio_transaction_repository.get_by_portfolio",
        return_value=[deposit],
    ):
        result = PortfolioTWRService.calculate(
            db=None,
            portfolio_id=portfolio_id,
        )

    assert result["period_count"] == 1
    assert result["periods"][0]["cash_flow"] == Decimal("1000")
    assert result["periods"][0]["return"] == Decimal("10.00")
    assert result["twr"] == Decimal("10.00")
    assert result["twr_pct"] == Decimal("10.00")
    
def test_twr_links_multiple_periods_with_external_deposit():
    portfolio_id = uuid4()

    snapshots = [
        type(
            "Snapshot",
            (),
            {
                "portfolio_value": Decimal("1000"),
                "snapshot_time": datetime(
                    2026,
                    1,
                    1,
                    tzinfo=timezone.utc,
                ),
            },
        )(),
        type(
            "Snapshot",
            (),
            {
                "portfolio_value": Decimal("1100"),
                "snapshot_time": datetime(
                    2026,
                    2,
                    1,
                    tzinfo=timezone.utc,
                ),
            },
        )(),
        type(
            "Snapshot",
            (),
            {
                "portfolio_value": Decimal("2400"),
                "snapshot_time": datetime(
                    2026,
                    3,
                    1,
                    tzinfo=timezone.utc,
                ),
            },
        )(),
    ]

    deposit = type(
        "Transaction",
        (),
        {
            "transaction_type": "DEPOSIT",
            "amount": Decimal("1000"),
            "transaction_date": datetime(
                2026,
                2,
                15,
                tzinfo=timezone.utc,
            ),
        },
    )()

    with patch(
        "services.portfolio_twr_service.portfolio_snapshot_repository.get_by_portfolio",
        return_value=snapshots,
    ), patch(
        "services.portfolio_twr_service.portfolio_transaction_repository.get_by_portfolio",
        return_value=[deposit],
    ):
        result = PortfolioTWRService.calculate(
            db=None,
            portfolio_id=portfolio_id,
        )

    assert result["snapshot_count"] == 3
    assert result["period_count"] == 2

    # Period 1: 1000 -> 1100 = +10%
    assert result["periods"][0]["return"] == Decimal("10.00")

    # Period 2: 1100 + 1000 deposit -> 2400 = +14.2857%
    assert result["periods"][1]["cash_flow"] == Decimal("1000")
    assert result["periods"][1]["return"] == Decimal("14.29")

    # Linked TWR = (1.10 * 1.142857...) - 1 = 25.714...%
    assert result["twr"] == Decimal("25.71")
    assert result["twr_pct"] == Decimal("25.71")