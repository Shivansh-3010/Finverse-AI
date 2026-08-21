from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from models.portfolio import Portfolio
from models.portfolio_transaction import (
    PortfolioTransaction,
    TransactionType,
)
from repositories.portfolio_transaction_repository import (
    portfolio_transaction_repository,
)
from schemas.portfolio_transaction import (
    PortfolioTransactionCreate,
)


class PortfolioTransactionService:
    """Business logic for immutable portfolio transactions."""

    def create_transaction(
        self,
        db: Session,
        data: PortfolioTransactionCreate,
    ) -> PortfolioTransaction:
        self._validate_transaction(data)

        portfolio = (
            db.query(Portfolio)
            .filter(Portfolio.id == data.portfolio_id)
            .first()
        )

        if portfolio is None:
            raise ValueError(
                f"Portfolio {data.portfolio_id} does not exist"
            )

        transaction = PortfolioTransaction(
            portfolio_id=data.portfolio_id,
            symbol=data.symbol.upper().strip(),
            transaction_type=data.transaction_type.upper().strip(),
            quantity=data.quantity,
            price=data.price,
            amount=data.amount,
            transaction_date=data.transaction_date,
            reference=data.reference,
        )

        return portfolio_transaction_repository.create(
            db,
            transaction,
        )

    def get_portfolio_transactions(
        self,
        db: Session,
        portfolio_id: UUID,
    ) -> list[PortfolioTransaction]:
        return portfolio_transaction_repository.get_by_portfolio(
            db,
            portfolio_id,
        )

    def get_symbol_transactions(
        self,
        db: Session,
        portfolio_id: UUID,
        symbol: str,
    ) -> list[PortfolioTransaction]:
        return portfolio_transaction_repository.get_by_symbol(
            db,
            portfolio_id,
            symbol.upper().strip(),
        )

    def get_transactions_by_date_range(
        self,
        db: Session,
        portfolio_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> list[PortfolioTransaction]:
        if start_date > end_date:
            raise ValueError(
                "start_date must be earlier than or equal to end_date"
            )

        return (
            portfolio_transaction_repository.get_by_date_range(
                db,
                portfolio_id,
                start_date,
                end_date,
            )
        )

    @staticmethod
    def _validate_transaction(
        data: PortfolioTransactionCreate,
    ) -> None:
        transaction_type = data.transaction_type.upper().strip()

        valid_types = {
            transaction.value
            for transaction in TransactionType
        }

        if transaction_type not in valid_types:
            raise ValueError(
                "Invalid transaction type. "
                f"Expected one of: {sorted(valid_types)}"
            )

        if not data.symbol.strip():
            raise ValueError(
                "Symbol cannot be empty"
            )

        if data.amount < Decimal("0"):
            raise ValueError(
                "Transaction amount cannot be negative"
            )

        if data.quantity is not None:
            if data.quantity <= Decimal("0"):
                raise ValueError(
                    "Quantity must be greater than zero"
                )

        if data.price is not None:
            if data.price < Decimal("0"):
                raise ValueError(
                    "Price cannot be negative"
                )

        if transaction_type in {
            TransactionType.BUY.value,
            TransactionType.SELL.value,
        }:
            if data.quantity is None:
                raise ValueError(
                    f"{transaction_type} transactions require quantity"
                )

            if data.price is None:
                raise ValueError(
                    f"{transaction_type} transactions require price"
                )

        if transaction_type == TransactionType.DIVIDEND.value:
            if data.amount <= Decimal("0"):
                raise ValueError(
                    "Dividend amount must be greater than zero"
                )
        
        if transaction_type in {
            TransactionType.DEPOSIT.value,
            TransactionType.WITHDRAWAL.value,
        }:
            if data.amount <= Decimal("0"):
                raise ValueError(
                    f"{transaction_type} amount must be greater than zero"
                )


portfolio_transaction_service = (
    PortfolioTransactionService()
)