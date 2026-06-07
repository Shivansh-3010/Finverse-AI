from sqlalchemy.orm import Session

from models.watchlist import Watchlist
from repositories.base_repository import BaseRepository


class WatchlistRepository(BaseRepository[Watchlist]):
    def __init__(self):
        super().__init__(Watchlist)

    def get_by_user(
        self,
        db: Session,
        user_id
    ):
        return (
            db.query(Watchlist)
            .filter(Watchlist.user_id == user_id)
            .all()
        )


watchlist_repository = WatchlistRepository()