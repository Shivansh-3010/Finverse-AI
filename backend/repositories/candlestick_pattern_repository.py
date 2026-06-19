from sqlalchemy import desc
from sqlalchemy.orm import Session

from models.candlestick_pattern import (
    CandlestickPattern,
)


class CandlestickPatternRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_latest(
        self,
        symbol: str
    ):
        return (
            self.db.query(CandlestickPattern)
            .filter(
                CandlestickPattern.symbol == symbol
            )
            .order_by(
                desc(CandlestickPattern.timestamp)
            )
            .first()
        )
        
    def get_latest_by_timeframe(
        self,
        symbol: str,
        timeframe: str
    ):
        return (
            self.db.query(CandlestickPattern)
            .filter(
                CandlestickPattern.symbol == symbol,
                CandlestickPattern.timeframe == timeframe
            )
            .order_by(
                desc(CandlestickPattern.timestamp)
            )
            .first()
        )

    def get_history(
        self,
        symbol: str
    ):
        return (
            self.db.query(CandlestickPattern)
            .filter(
                CandlestickPattern.symbol == symbol
            )
            .order_by(
                CandlestickPattern.timestamp
            )
            .all()
        )
        
    def get_history_by_timeframe(
        self,
        symbol: str,
        timeframe: str
    ):
        return (
            self.db.query(CandlestickPattern)
            .filter(
                CandlestickPattern.symbol == symbol,
                CandlestickPattern.timeframe == timeframe
            )
            .order_by(
                CandlestickPattern.timestamp
            )
            .all()
        )

    def save(
        self,
        pattern: CandlestickPattern
    ):
        saved_pattern = self.db.merge(pattern)

        self.db.commit()
        self.db.refresh(saved_pattern)

        return saved_pattern
    
    def bulk_insert(
        self,
        patterns: list,
    ):

        self.db.bulk_save_objects(
            patterns
        )

        self.db.commit()
        
    def get_existing_timestamps(
        self,
        symbol: str,
        timeframe: str,
    ):

        rows = (
            self.db.query(
                CandlestickPattern.timestamp
            )
            .filter(
                CandlestickPattern.symbol == symbol,
                CandlestickPattern.timeframe == timeframe,
            )
            .distinct()
            .all()
        )

        return {
            row[0]
            for row in rows
        }