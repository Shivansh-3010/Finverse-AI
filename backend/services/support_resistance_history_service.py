from database.session import SessionLocal

from repositories.support_resistance_repository import (
    SupportResistanceRepository,
)


class SupportResistanceHistoryService:

    @staticmethod
    def get_history(
        symbol: str,
        timeframe: str = "1d",
    ):

        db = SessionLocal()

        try:

            repository = (
                SupportResistanceRepository(
                    db
                )
            )

            history = (
                repository
                .get_history_by_timeframe(
                    symbol=symbol,
                    timeframe=timeframe,
                )
            )

            return {
                "history": history
            }

        finally:
            db.close()