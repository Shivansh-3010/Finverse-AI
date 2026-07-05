from sqlalchemy import func
from sqlalchemy.orm import Session

from models.ohlcv_data import OHLCVData


class UniverseSelector:

    @staticmethod
    def get_symbols(
        db: Session,
        timeframe: str = "1d",
        min_candles: int = 5000,
    ) -> list[str]:

        rows = (
            db.query(
                OHLCVData.symbol,
                func.count().label("count")
            )
            .filter(
                OHLCVData.timeframe == timeframe
            )
            .group_by(
                OHLCVData.symbol
            )
            .having(
                func.count() >= min_candles
            )
            .all()
        )

        return [
            row.symbol
            for row in rows
        ]