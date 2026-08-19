from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from sqlalchemy.orm import Session

from models.portfolio_transaction import (
    TransactionType,
)
from repositories.portfolio_transaction_repository import (
    portfolio_transaction_repository,
)


def _money(value: Decimal) -> Decimal:
    return value.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


class PortfolioPerformanceService:
    """Calculate portfolio performance from the transaction ledger."""

    @staticmethod
    def calculate(
        db: Session,
        portfolio_id: UUID,
    ) -> dict:

        transactions = (
            portfolio_transaction_repository.get_by_portfolio(
                db,
                portfolio_id,
            )
        )

        positions = {}

        realized_pnl = Decimal("0")
        dividend_income = Decimal("0")
        total_bought = Decimal("0")
        total_sold = Decimal("0")

        for transaction in transactions:

            symbol = transaction.symbol.upper()
            transaction_type = transaction.transaction_type

            if symbol not in positions:
                positions[symbol] = {
                    "quantity": Decimal("0"),
                    "cost_basis": Decimal("0"),
                }

            position = positions[symbol]

            if transaction_type == TransactionType.BUY.value:

                quantity = transaction.quantity or Decimal("0")
                amount = transaction.amount

                position["quantity"] += quantity
                position["cost_basis"] += amount

                total_bought += amount

            elif transaction_type == TransactionType.SELL.value:

                quantity = transaction.quantity or Decimal("0")
                amount = transaction.amount

                current_quantity = position["quantity"]
                current_cost_basis = position["cost_basis"]

                if quantity > current_quantity:
                    raise ValueError(
                        f"SELL quantity for {symbol} exceeds "
                        "current holding"
                    )

                average_cost = (
                    current_cost_basis / current_quantity
                    if current_quantity > Decimal("0")
                    else Decimal("0")
                )

                cost_of_sold_quantity = (
                    average_cost * quantity
                )

                realized_pnl += (
                    amount - cost_of_sold_quantity
                )

                position["quantity"] -= quantity
                position["cost_basis"] -= (
                    cost_of_sold_quantity
                )

                total_sold += amount

            elif transaction_type == TransactionType.DIVIDEND.value:

                dividend_income += transaction.amount

            elif transaction_type == TransactionType.SPLIT.value:

                quantity = transaction.quantity or Decimal("0")

                if quantity > Decimal("0"):
                    position["quantity"] += quantity

            elif transaction_type == TransactionType.BONUS.value:

                quantity = transaction.quantity or Decimal("0")

                if quantity > Decimal("0"):
                    position["quantity"] += quantity

        active_positions = {}

        for symbol, position in positions.items():

            quantity = position["quantity"]
            cost_basis = position["cost_basis"]

            if quantity > Decimal("0"):

                average_cost = (
                    cost_basis / quantity
                )

                active_positions[symbol] = {
                    "quantity": quantity,
                    "cost_basis": _money(
                        cost_basis
                    ),
                    "avg_price": _money(
                        average_cost
                    ),
                }

        total_realized_return = (
            realized_pnl + dividend_income
        )
        
        net_cash_flow = (
            total_sold
            + dividend_income
            - total_bought
        )

        return {
            "portfolio_id": portfolio_id,

            "transactions": len(transactions),

            "total_bought": _money(
                total_bought
            ),

            "total_sold": _money(
                total_sold
            ),

            "realized_pnl": _money(
                realized_pnl
            ),

            "dividend_income": _money(
                dividend_income
            ),

            "total_realized_return": _money(
                total_realized_return
            ),
            
            "net_cash_flow": _money(
                net_cash_flow
            ),

            "positions": active_positions,
        }


portfolio_performance_service = (
    PortfolioPerformanceService()
)