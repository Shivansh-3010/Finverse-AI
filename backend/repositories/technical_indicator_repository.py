from sqlalchemy import desc
from sqlalchemy.orm import Session

from models.technical_indicator import TechnicalIndicator


class TechnicalIndicatorRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_latest(
        self,
        symbol: str
    ):
        return (
            self.db.query(TechnicalIndicator)
            .filter(
                TechnicalIndicator.symbol == symbol
            )
            .order_by(
                desc(TechnicalIndicator.timestamp)
            )
            .first()
        )
        
    def get_latest_by_timeframe(
        self,
        symbol: str,
        timeframe: str
    ):
        return (
            self.db.query(TechnicalIndicator)
            .filter(
                TechnicalIndicator.symbol == symbol,
                TechnicalIndicator.timeframe == timeframe
            )
            .order_by(
                desc(TechnicalIndicator.timestamp)
            )
            .first()
        )

    def get_history(
        self,
        symbol: str
    ):
        return (
            self.db.query(TechnicalIndicator)
            .filter(
                TechnicalIndicator.symbol == symbol
            )
            .order_by(
                TechnicalIndicator.timestamp
            )
            .all()
        )
        
    def get_history_by_timeframe(
        self,
        symbol: str,
        timeframe: str
    ):
        return (
            self.db.query(TechnicalIndicator)
            .filter(
                TechnicalIndicator.symbol == symbol,
                TechnicalIndicator.timeframe == timeframe
            )
            .order_by(
                TechnicalIndicator.timestamp
            )
            .all()
        )
        
    def save(
        self,
        indicator: TechnicalIndicator
    ):
        saved_indicator = self.db.merge(indicator)

        self.db.commit()
        self.db.refresh(saved_indicator)

        return saved_indicator