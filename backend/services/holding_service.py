from collections import defaultdict
from decimal import Decimal

from sqlalchemy.orm import Session

from models.portfolio_transaction import (
    PortfolioTransaction,
    TransactionType,
)
from repositories.holding_repository import (
    holding_repository,
)
from repositories.portfolio_transaction_repository import (
    portfolio_transaction_repository,
)


class HoldingService:

    @staticmethod
    def create(
        db,
        portfolio_id,
        symbol,
        quantity,
        avg_price,
        current_price,
        market_value,
    ):
        holding = holding_repository.model(
            portfolio_id=portfolio_id,
            symbol=symbol.upper().strip(),
            quantity=quantity,
            avg_price=avg_price,
            current_price=current_price,
            market_value=market_value,
        )

        return holding_repository.create(
            db,
            holding,
        )

    @staticmethod
    def get_by_portfolio(
        db,
        portfolio_id,
    ):
        return holding_repository.get_by_portfolio(
            db,
            portfolio_id,
        )

    @staticmethod
    def calculate_from_transactions(
        db: Session,
        portfolio_id,
    ):
        transactions = (
            portfolio_transaction_repository
            .get_by_portfolio(
                db,
                portfolio_id,
            )
        )

        positions = defaultdict(
            lambda: {
                "quantity": Decimal("0"),
                "cost_basis": Decimal("0"),
            }
        )

        for transaction in transactions:

            symbol = transaction.symbol.upper().strip()
            transaction_type = (
                transaction.transaction_type
            )

            position = positions[symbol]

            quantity = (
                transaction.quantity
                or Decimal("0")
            )

            amount = (
                transaction.amount
                or Decimal("0")
            )

            price = (
                transaction.price
                or Decimal("0")
            )

            if transaction_type == TransactionType.BUY.value:

                position["quantity"] += quantity
                position["cost_basis"] += amount

            elif transaction_type == TransactionType.SELL.value:

                current_quantity = (
                    position["quantity"]
                )

                if current_quantity <= Decimal("0"):
                    continue

                average_cost = (
                    position["cost_basis"]
                    / current_quantity
                )

                position["quantity"] -= quantity

                position["cost_basis"] -= (
                    average_cost * quantity
                )

                if position["quantity"] <= Decimal("0"):
                    position["quantity"] = Decimal("0")
                    position["cost_basis"] = Decimal("0")

            elif transaction_type == TransactionType.SPLIT.value:

                if quantity > Decimal("0"):
                    position["quantity"] *= quantity

            elif transaction_type == TransactionType.BONUS.value:

                position["quantity"] += quantity

        holdings = []

        for symbol, position in positions.items():

            quantity = position["quantity"]
            cost_basis = position["cost_basis"]

            if quantity <= Decimal("0"):
                continue

            avg_price = (
                cost_basis / quantity
                if quantity > Decimal("0")
                else Decimal("0")
            )

            holdings.append(
                {
                    "portfolio_id": portfolio_id,
                    "symbol": symbol,
                    "quantity": quantity,
                    "avg_price": avg_price,
                    "cost_basis": cost_basis,
                }
            )

        return holdings


holding_service = HoldingService()