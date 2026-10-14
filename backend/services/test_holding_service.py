from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from models.portfolio_transaction import TransactionType
from services.holding_service import HoldingService


def make_transaction(
    transaction_type: str,
    quantity: str | None,
    amount: str = "0",
    symbol: str = "RELIANCE",
):
    transaction = MagicMock()
    transaction.symbol = symbol
    transaction.transaction_type = transaction_type
    transaction.quantity = (
        Decimal(quantity) if quantity is not None else None
    )
    transaction.amount = Decimal(amount)
    transaction.transaction_date = datetime.now(timezone.utc)
    return transaction


def calculate_holdings(transactions):
    portfolio_id = uuid4()

    with patch(
        "services.holding_service.portfolio_transaction_repository.get_by_portfolio",
        return_value=transactions,
    ):
        holdings = HoldingService.calculate_from_transactions(
            db=None,
            portfolio_id=portfolio_id,
        )

    return portfolio_id, holdings


def test_buy_calculates_quantity_and_cost_basis():
    transaction = make_transaction(
        TransactionType.BUY.value,
        quantity="10",
        amount="15000",
    )

    portfolio_id, holdings = calculate_holdings([transaction])

    assert len(holdings) == 1
    assert holdings[0]["portfolio_id"] == portfolio_id
    assert holdings[0]["symbol"] == "RELIANCE"
    assert holdings[0]["quantity"] == Decimal("10")
    assert holdings[0]["cost_basis"] == Decimal("15000")
    assert holdings[0]["avg_price"] == Decimal("1500")


def test_sell_reduces_quantity_and_cost_basis_proportionally():
    transactions = [
        make_transaction("BUY", "10", "15000"),
        make_transaction("SELL", "4", "6400"),
    ]

    _, holdings = calculate_holdings(transactions)

    assert len(holdings) == 1
    assert holdings[0]["quantity"] == Decimal("6")
    assert holdings[0]["cost_basis"] == Decimal("9000")
    assert holdings[0]["avg_price"] == Decimal("1500")


def test_sell_exceeding_current_holding_raises_value_error():
    transactions = [
        make_transaction("BUY", "5", "5000"),
        make_transaction("SELL", "6", "6000"),
    ]

    with pytest.raises(ValueError, match="SELL quantity for RELIANCE exceeds current holding"):
        calculate_holdings(transactions)


def test_sell_after_all_shares_are_sold_excludes_position():
    transactions = [
        make_transaction("BUY", "5", "5000"),
        make_transaction("SELL", "5", "6000"),
    ]

    _, holdings = calculate_holdings(transactions)

    assert holdings == []


def test_split_changes_quantity_without_changing_cost_basis():
    transactions = [
        make_transaction("BUY", "10", "15000"),
        make_transaction("SPLIT", "2"),
    ]

    _, holdings = calculate_holdings(transactions)

    assert holdings[0]["quantity"] == Decimal("20")
    assert holdings[0]["cost_basis"] == Decimal("15000")
    assert holdings[0]["avg_price"] == Decimal("750")


def test_bonus_increases_quantity_without_changing_cost_basis():
    transactions = [
        make_transaction("BUY", "10", "15000"),
        make_transaction("BONUS", "5"),
    ]

    _, holdings = calculate_holdings(transactions)

    assert holdings[0]["quantity"] == Decimal("15")
    assert holdings[0]["cost_basis"] == Decimal("15000")
    assert holdings[0]["avg_price"] == Decimal("1000")


def test_zero_or_negative_split_multiplier_is_ignored():
    transactions = [
        make_transaction("BUY", "10", "15000"),
        make_transaction("SPLIT", "0"),
        make_transaction("SPLIT", "-2"),
    ]

    _, holdings = calculate_holdings(transactions)

    assert holdings[0]["quantity"] == Decimal("10")
    assert holdings[0]["cost_basis"] == Decimal("15000")


def test_zero_or_negative_bonus_quantity_is_ignored():
    transactions = [
        make_transaction("BUY", "10", "15000"),
        make_transaction("BONUS", "0"),
        make_transaction("BONUS", "-2"),
    ]

    _, holdings = calculate_holdings(transactions)

    assert holdings[0]["quantity"] == Decimal("10")
    assert holdings[0]["cost_basis"] == Decimal("15000")


def test_sell_without_existing_holding_is_ignored():
    transactions = [
        make_transaction("SELL", "2", "2000"),
    ]

    _, holdings = calculate_holdings(transactions)

    assert holdings == []


def test_symbols_are_normalized_and_aggregated():
    transactions = [
        make_transaction("BUY", "2", "2000", "reliance"),
        make_transaction("BUY", "3", "3600", " RELIANCE "),
    ]

    _, holdings = calculate_holdings(transactions)

    assert len(holdings) == 1
    assert holdings[0]["symbol"] == "RELIANCE"
    assert holdings[0]["quantity"] == Decimal("5")
    assert holdings[0]["cost_basis"] == Decimal("5600")
    assert holdings[0]["avg_price"] == Decimal("1120")
