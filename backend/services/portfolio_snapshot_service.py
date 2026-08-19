from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from models.portfolio_snapshot import PortfolioSnapshot
from repositories.portfolio_snapshot_repository import (
    portfolio_snapshot_repository,
)


class PortfolioSnapshotService:
    """Business logic for portfolio snapshots."""

    @staticmethod
    def create(
        db: Session,
        portfolio_id: UUID,
        snapshot_time: datetime,
        portfolio_value: Decimal,
        cash: Decimal,
        invested_value: Decimal,
        return_value: Decimal,
        risk_score: Decimal | None = None,
    ) -> PortfolioSnapshot:

        if portfolio_value < Decimal("0"):
            raise ValueError(
                "Portfolio value cannot be negative"
            )

        if cash < Decimal("0"):
            raise ValueError(
                "Cash cannot be negative"
            )

        if invested_value < Decimal("0"):
            raise ValueError(
                "Invested value cannot be negative"
            )

        return_value = Decimal(return_value)

        snapshot = PortfolioSnapshot(
            portfolio_id=portfolio_id,
            snapshot_time=snapshot_time,
            portfolio_value=portfolio_value,
            cash=cash,
            invested_value=invested_value,
            return_value=return_value,
            risk_score=risk_score,
        )

        return portfolio_snapshot_repository.create(
            db,
            snapshot,
        )

    @staticmethod
    def get_by_portfolio(
        db: Session,
        portfolio_id: UUID,
    ) -> list[PortfolioSnapshot]:
        return portfolio_snapshot_repository.get_by_portfolio(
            db,
            portfolio_id,
        )

    @staticmethod
    def get_by_date_range(
        db: Session,
        portfolio_id: UUID,
        start_time: datetime,
        end_time: datetime,
    ) -> list[PortfolioSnapshot]:

        if start_time > end_time:
            raise ValueError(
                "start_time must be earlier than or equal to end_time"
            )

        return portfolio_snapshot_repository.get_by_date_range(
            db,
            portfolio_id,
            start_time,
            end_time,
        )

    @staticmethod
    def get_latest(
        db: Session,
        portfolio_id: UUID,
    ):
        return portfolio_snapshot_repository.get_latest(
            db,
            portfolio_id,
        )


portfolio_snapshot_service = PortfolioSnapshotService()