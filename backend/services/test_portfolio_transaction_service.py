from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock, patch
from uuid import uuid4

from models.portfolio_transaction import PortfolioTransaction
import pytest

from models.portfolio import Portfolio
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
def test_sell_without_holdings_is_rejected_before_save():
    data = make_transaction("SELL")
    db = MagicMock()

    query = db.query.return_value
    query.filter.return_value.first.return_value = MagicMock(
        spec=Portfolio
    )

    with (
        patch(
            "services.portfolio_transaction_service."
            "portfolio_transaction_repository.get_by_symbol",
            return_value=[],
        ),
        patch(
            "services.portfolio_transaction_service."
            "portfolio_transaction_repository.create",
        ) as create_transaction,
        pytest.raises(
            ValueError,
            match="SELL quantity for RELIANCE exceeds current holding",
        ),
    ):
        service.create_transaction(db, data)

    create_transaction.assert_not_called()

def test_valid_buy_then_sell_is_allowed():
    portfolio_id = uuid4()
    buy_date = datetime(2026, 1, 1, tzinfo=timezone.utc)
    sell_date = datetime(2026, 1, 2, tzinfo=timezone.utc)

    buy = MagicMock()
    buy.symbol = "RELIANCE"
    buy.transaction_type = "BUY"
    buy.quantity = Decimal("10")
    buy.transaction_date = buy_date
    buy.id = uuid4()

    data = make_transaction(
        "SELL",
        portfolio_id=portfolio_id,
        quantity=Decimal("4"),
        transaction_date=sell_date,
    )
    db = MagicMock()
    db.query.return_value.filter.return_value.with_for_update.return_value.first.return_value = MagicMock(
        spec=Portfolio
    )

    with (
        patch(
            "services.portfolio_transaction_service."
            "portfolio_transaction_repository.get_by_symbol",
            return_value=[buy],
        ),
        patch(
            "services.portfolio_transaction_service."
            "portfolio_transaction_repository.create",
            side_effect=lambda _db, transaction: transaction,
        ) as create_transaction,
    ):
        result = service.create_transaction(db, data)

    assert result.transaction_type == "SELL"
    create_transaction.assert_called_once()

def test_sell_exceeding_existing_holding_is_rejected():
    data = make_transaction(
        "SELL",
        quantity=Decimal("6"),
    )
    db = MagicMock()
    db.query.return_value.filter.return_value.with_for_update.return_value.first.return_value = MagicMock(
        spec=Portfolio
    )

    buy = MagicMock()
    buy.symbol = "RELIANCE"
    buy.transaction_type = "BUY"
    buy.quantity = Decimal("5")
    buy.transaction_date = datetime(2026, 1, 1, tzinfo=timezone.utc)
    buy.id = uuid4()

    with (
        patch(
            "services.portfolio_transaction_service."
            "portfolio_transaction_repository.get_by_symbol",
            return_value=[buy],
        ),
        patch(
            "services.portfolio_transaction_service."
            "portfolio_transaction_repository.create",
        ) as create_transaction,
        pytest.raises(ValueError, match="exceeds current holding"),
    ):
        service.create_transaction(db, data)

    create_transaction.assert_not_called()

def test_historical_sell_cannot_invalidate_later_sell():
    first_buy = MagicMock()
    first_buy.symbol = "RELIANCE"
    first_buy.transaction_type = "BUY"
    first_buy.quantity = Decimal("10")
    first_buy.transaction_date = datetime(2026, 1, 1, tzinfo=timezone.utc)
    first_buy.id = uuid4()

    later_sell = MagicMock()
    later_sell.symbol = "RELIANCE"
    later_sell.transaction_type = "SELL"
    later_sell.quantity = Decimal("8")
    later_sell.transaction_date = datetime(2026, 1, 10, tzinfo=timezone.utc)
    later_sell.id = uuid4()

    historical_sell = MagicMock()
    historical_sell.symbol = "RELIANCE"
    historical_sell.transaction_type = "SELL"
    historical_sell.quantity = Decimal("5")
    historical_sell.transaction_date = datetime(2026, 1, 5, tzinfo=timezone.utc)
    historical_sell.id = uuid4()

    with pytest.raises(ValueError, match="exceeds current holding"):
        service._validate_sell_against_ledger(
            [first_buy, later_sell],
            historical_sell,
        )

def test_historical_buy_that_invalidates_later_sell_is_rejected():
    portfolio_id = uuid4()

    later_buy = MagicMock()
    later_buy.symbol = "RELIANCE"
    later_buy.transaction_type = "BUY"
    later_buy.quantity = Decimal("5")
    later_buy.transaction_date = datetime(
        2026, 1, 8, tzinfo=timezone.utc
    )
    later_buy.id = uuid4()

    later_sell = MagicMock()
    later_sell.symbol = "RELIANCE"
    later_sell.transaction_type = "SELL"
    later_sell.quantity = Decimal("8")
    later_sell.transaction_date = datetime(
        2026, 1, 10, tzinfo=timezone.utc
    )
    later_sell.id = uuid4()

    historical_buy = MagicMock()
    historical_buy.symbol = "RELIANCE"
    historical_buy.transaction_type = "BUY"
    historical_buy.quantity = Decimal("2")
    historical_buy.transaction_date = datetime(
        2026, 1, 5, tzinfo=timezone.utc
    )
    historical_buy.id = uuid4()

    with pytest.raises(
        ValueError,
        match="exceeds current holding",
    ):
        service._validate_sell_against_ledger(
            [later_buy, later_sell],
            historical_buy,
        )


def test_sell_after_split_uses_adjusted_quantity():
    buy = MagicMock()
    buy.symbol = "RELIANCE"
    buy.transaction_type = "BUY"
    buy.quantity = Decimal("5")
    buy.transaction_date = datetime(
        2026, 1, 1, tzinfo=timezone.utc
    )
    buy.id = uuid4()

    split = MagicMock()
    split.symbol = "RELIANCE"
    split.transaction_type = "SPLIT"
    split.quantity = Decimal("2")
    split.transaction_date = datetime(
        2026, 1, 5, tzinfo=timezone.utc
    )
    split.id = uuid4()

    proposed_sell = MagicMock()
    proposed_sell.symbol = "RELIANCE"
    proposed_sell.transaction_type = "SELL"
    proposed_sell.quantity = Decimal("8")
    proposed_sell.transaction_date = datetime(
        2026, 1, 10, tzinfo=timezone.utc
    )
    proposed_sell.id = None

    service._validate_sell_against_ledger(
        [buy, split],
        proposed_sell,
    )

def test_sell_after_bonus_uses_adjusted_quantity():
    portfolio_id = uuid4()

    buy = MagicMock()
    buy.symbol = "RELIANCE"
    buy.transaction_type = "BUY"
    buy.quantity = Decimal("5")
    buy.transaction_date = datetime(
        2026, 1, 1, tzinfo=timezone.utc
    )
    buy.id = uuid4()

    bonus = MagicMock()
    bonus.symbol = "RELIANCE"
    bonus.transaction_type = "BONUS"
    bonus.quantity = Decimal("3")
    bonus.transaction_date = datetime(
        2026, 1, 5, tzinfo=timezone.utc
    )
    bonus.id = uuid4()

    proposed_sell = MagicMock()
    proposed_sell.symbol = "RELIANCE"
    proposed_sell.transaction_type = "SELL"
    proposed_sell.quantity = Decimal("8")
    proposed_sell.transaction_date = datetime(
        2026, 1, 10, tzinfo=timezone.utc
    )
    proposed_sell.id = None

    service._validate_sell_against_ledger(
        [buy, bonus],
        proposed_sell,
    )
