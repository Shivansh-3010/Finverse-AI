from database.session import SessionLocal

from repositories.technical_indicator_repository import (
    TechnicalIndicatorRepository,
)
from utils.timeframe_validator import (
    validate_timeframe,
)


class TechnicalIndicatorService:

    @staticmethod
    def get_latest(symbol: str,
                   timeframe: str = "1d"
                ):
        
        validate_timeframe(
            timeframe
        )

        db = SessionLocal()

        try:
            repository = TechnicalIndicatorRepository(db)

            return repository.get_latest_by_timeframe(
                symbol=symbol,
                timeframe=timeframe
            )

        finally:
            db.close()

    @staticmethod
    def get_history(symbol: str,
                    timeframe: str = "1d"
                ):
        
        validate_timeframe(
            timeframe
        )

        db = SessionLocal()

        try:
            repository = TechnicalIndicatorRepository(db)

            return {
                "indicators":
                    repository.get_history_by_timeframe(
                        symbol=symbol,
                        timeframe=timeframe
                    )
            }

        finally:
            db.close()