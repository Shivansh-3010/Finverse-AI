from datetime import datetime, timezone

from database.session import SessionLocal
from models.candlestick_pattern import (
    CandlestickPattern,
)
from repositories.candlestick_pattern_repository import (
    CandlestickPatternRepository,
)


class CandlestickPatternPersistenceService:

    @staticmethod
    def save_patterns(
        symbol: str,
        candlestick_score: float,
        patterns: list,
    ):

        db = SessionLocal()

        try:

            repository = (
                CandlestickPatternRepository(db)
            )

            saved_patterns = []

            for pattern in patterns:

                entity = CandlestickPattern(
                    symbol=symbol,
                    timestamp=datetime.now(
                        timezone.utc
                    ),

                    pattern_name=pattern["pattern"],
                    signal=pattern["signal"].value,
                    strength=pattern["strength"],

                    candlestick_score=
                        candlestick_score,
                )

                saved_patterns.append(
                    repository.save(entity)
                )

            return saved_patterns

        finally:
            db.close()