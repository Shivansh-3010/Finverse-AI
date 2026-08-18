from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from models.portfolio_transaction import PortfolioTransaction
from repositories.base_repository import BaseRepository


class PortfolioTransactionRepository(
    BaseRepository[PortfolioTransaction]
):
    def __init__(self):
        super().__init__(PortfolioTransaction)

    def get_by_portfolio(
        self,
        db: Session,
        portfolio_id: UUID,
    ) -> list[PortfolioTransaction]:
        return (
            db.query(PortfolioTransaction)
            .filter(
                PortfolioTransaction.portfolio_id == portfolio_id
            )
            .order_by(
                PortfolioTransaction.transaction_date.asc()
            )
            .all()
        )

    def get_by_symbol(
        self,
        db: Session,
        portfolio_id: UUID,
        symbol: str,
    ) -> list[PortfolioTransaction]:
        return (
            db.query(PortfolioTransaction)
            .filter(
                PortfolioTransaction.portfolio_id == portfolio_id,
                PortfolioTransaction.symbol == symbol,
            )
            .order_by(
                PortfolioTransaction.transaction_date.asc()
            )
            .all()
        )

    def get_by_date_range(
        self,
        db: Session,
        portfolio_id: UUID,
        start_date: datetime,
        end_date: datetime,
    ) -> list[PortfolioTransaction]:
        return (
            db.query(PortfolioTransaction)
            .filter(
                PortfolioTransaction.portfolio_id == portfolio_id,
                PortfolioTransaction.transaction_date >= start_date,
                PortfolioTransaction.transaction_date <= end_date,
            )
            .order_by(
                PortfolioTransaction.transaction_date.asc()
            )
            .all()
        )


portfolio_transaction_repository = (
    PortfolioTransactionRepository()
)