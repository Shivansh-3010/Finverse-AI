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
    
    def bulk_insert(
        self,
        indicators: list
    ):

        self.db.bulk_save_objects(
            indicators
        )

        self.db.commit()
        
    def exists(
        self,
        symbol: str,
        timeframe: str,
        timestamp,
    ):

        return (
            self.db.query(
                TechnicalIndicator
            )
            .filter(
                TechnicalIndicator.symbol == symbol,

                TechnicalIndicator.timeframe == timeframe,

                TechnicalIndicator.timestamp == timestamp,
            )
            .first()
            is not None
        )
        
    def get_existing_timestamps(
        self,
        symbol: str,
        timeframe: str
    ):

        rows = (
            self.db.query(
                TechnicalIndicator.timestamp
            )
            .filter(
                TechnicalIndicator.symbol == symbol,
                TechnicalIndicator.timeframe == timeframe
            )
            .all()
        )

        return {
            row[0]
            for row in rows
        }