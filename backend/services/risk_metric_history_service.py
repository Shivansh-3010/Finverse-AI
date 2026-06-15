from database.session import SessionLocal

from repositories.risk_metric_repository import (
    RiskMetricRepository,
)


class RiskMetricHistoryService:

    @staticmethod
    def get_history(
        symbol: str,
        timeframe: str = "1d"
    ):

        db = SessionLocal()

        try:

            repository = (
                RiskMetricRepository(db)
            )

            return {
                "metrics":
                    repository.get_history(
                        symbol=symbol,
                        timeframe=timeframe
                    )
            }

        finally:
            db.close()