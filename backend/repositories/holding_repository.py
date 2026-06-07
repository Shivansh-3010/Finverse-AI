from sqlalchemy.orm import Session

from models.holding import Holding
from repositories.base_repository import BaseRepository


class HoldingRepository(BaseRepository[Holding]):
    def __init__(self):
        super().__init__(Holding)

    def get_by_portfolio(
        self,
        db: Session,
        portfolio_id
    ):
        return (
            db.query(Holding)
            .filter(Holding.portfolio_id == portfolio_id)
            .all()
        )


holding_repository = HoldingRepository()