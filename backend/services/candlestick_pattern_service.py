from database.session import SessionLocal

from repositories.candlestick_pattern_repository import (
    CandlestickPatternRepository,
)
from utils.timeframe_validator import (
    validate_timeframe,
)


class CandlestickPatternService:

    @staticmethod
    def get_history(
        symbol: str,
        timeframe: str = "1d"
    ):
        
        validate_timeframe(
            timeframe
        )

        db = SessionLocal()

        try:

            repository = (
                CandlestickPatternRepository(db)
            )

            patterns = (
                repository.get_history_by_timeframe(
                    symbol=symbol,
                    timeframe=timeframe
                )
            )

            return {
                "patterns": patterns
            }

        finally:
            db.close()