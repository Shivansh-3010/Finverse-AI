from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from models.portfolio_snapshot import PortfolioSnapshot
from repositories.base_repository import BaseRepository


class PortfolioSnapshotRepository(
    BaseRepository[PortfolioSnapshot]
):
    def __init__(self):
        super().__init__(PortfolioSnapshot)

    def get_by_portfolio(
        self,
        db: Session,
        portfolio_id: UUID,
    ) -> list[PortfolioSnapshot]:
        return (
            db.query(PortfolioSnapshot)
            .filter(
                PortfolioSnapshot.portfolio_id
                == portfolio_id
            )
            .order_by(
                PortfolioSnapshot.snapshot_time.asc()
            )
            .all()
        )

    def get_by_date_range(
        self,
        db: Session,
        portfolio_id: UUID,
        start_time: datetime,
        end_time: datetime,
    ) -> list[PortfolioSnapshot]:
        return (
            db.query(PortfolioSnapshot)
            .filter(
                PortfolioSnapshot.portfolio_id
                == portfolio_id,
                PortfolioSnapshot.snapshot_time
                >= start_time,
                PortfolioSnapshot.snapshot_time
                <= end_time,
            )
            .order_by(
                PortfolioSnapshot.snapshot_time.asc()
            )
            .all()
        )

    def get_latest(
        self,
        db: Session,
        portfolio_id: UUID,
    ):
        return (
            db.query(PortfolioSnapshot)
            .filter(
                PortfolioSnapshot.portfolio_id
                == portfolio_id
            )
            .order_by(
                PortfolioSnapshot.snapshot_time.desc()
            )
            .first()
        )


portfolio_snapshot_repository = (
    PortfolioSnapshotRepository()
)