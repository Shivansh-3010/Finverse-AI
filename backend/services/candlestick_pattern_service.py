from database.session import SessionLocal

from repositories.candlestick_pattern_repository import (
    CandlestickPatternRepository,
)


class CandlestickPatternService:

    @staticmethod
    def get_history(
        symbol: str
    ):

        db = SessionLocal()

        try:

            repository = (
                CandlestickPatternRepository(db)
            )

            patterns = repository.get_history(
                symbol
            )

            return {
                "patterns": patterns
            }

        finally:
            db.close()