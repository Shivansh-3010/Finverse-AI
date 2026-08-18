from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

import pytest

from schemas.portfolio_transaction import (
    PortfolioTransactionCreate,
)
from services.portfolio_transaction_service import (
    PortfolioTransactionService,
)


service = PortfolioTransactionService()


def make_transaction(
    transaction_type: str = "BUY",
    **overrides,
) -> PortfolioTransactionCreate:
    data = {
        "portfolio_id": uuid4(),
        "symbol": "RELIANCE",
        "transaction_type": transaction_type,
        "quantity": Decimal("10"),
        "price": Decimal("1500.00"),
        "amount": Decimal("15000.00"),
        "transaction_date": datetime.now(timezone.utc),
        "reference": "TEST",
    }

    data.update(overrides)

    return PortfolioTransactionCreate(**data)


def test_valid_buy_transaction():
    data = make_transaction("BUY")

    service._validate_transaction(data)


def test_valid_sell_transaction():
    data = make_transaction("SELL")

    service._validate_transaction(data)


def test_valid_dividend_transaction():
    data = make_transaction(
        "DIVIDEND",
        quantity=None,
        price=None,
        amount=Decimal("500.00"),
    )

    service._validate_transaction(data)


def test_invalid_transaction_type():
    data = make_transaction("INVALID")

    with pytest.raises(
        ValueError,
        match="Invalid transaction type",
    ):
        service._validate_transaction(data)


def test_buy_requires_quantity():
    data = make_transaction(
        "BUY",
        quantity=None,
    )

    with pytest.raises(
        ValueError,
        match="BUY transactions require quantity",
    ):
        service._validate_transaction(data)


def test_buy_requires_price():
    data = make_transaction(
        "BUY",
        price=None,
    )

    with pytest.raises(
        ValueError,
        match="BUY transactions require price",
    ):
        service._validate_transaction(data)


def test_negative_amount_rejected():
    data = make_transaction(
        "BUY",
        amount=Decimal("-100"),
    )

    with pytest.raises(
        ValueError,
        match="Transaction amount cannot be negative",
    ):
        service._validate_transaction(data)


def test_zero_quantity_rejected():
    data = make_transaction(
        "BUY",
        quantity=Decimal("0"),
    )

    with pytest.raises(
        ValueError,
        match="Quantity must be greater than zero",
    ):
        service._validate_transaction(data)


def test_negative_price_rejected():
    data = make_transaction(
        "BUY",
        price=Decimal("-10"),
    )

    with pytest.raises(
        ValueError,
        match="Price cannot be negative",
    ):
        service._validate_transaction(data)


def test_invalid_date_range():
    start_date = datetime(
        2026,
        8,
        20,
        tzinfo=timezone.utc,
    )

    end_date = datetime(
        2026,
        8,
        10,
        tzinfo=timezone.utc,
    )

    with pytest.raises(
        ValueError,
        match="start_date must be earlier",
    ):
        service.get_transactions_by_date_range(
            db=None,
            portfolio_id=uuid4(),
            start_date=start_date,
            end_date=end_date,
        )