from sqlalchemy.orm import Session

from models.portfolio import Portfolio
from repositories.base_repository import BaseRepository


class PortfolioRepository(BaseRepository[Portfolio]):
    def __init__(self):
        super().__init__(Portfolio)

    def get_by_user(
        self,
        db: Session,
        user_id
    ):
        return (
            db.query(Portfolio)
            .filter(Portfolio.user_id == user_id)
            .all()
        )


portfolio_repository = PortfolioRepository()