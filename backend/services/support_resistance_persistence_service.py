from datetime import datetime, timezone

from database.session import SessionLocal

from models.support_resistance import (
    SupportResistance,
)

from repositories.support_resistance_repository import (
    SupportResistanceRepository,
)


class SupportResistancePersistenceService:

    @staticmethod
    def save_snapshot(
        symbol: str,
        timeframe: str,
        analysis: dict,
    ):

        db = SessionLocal()

        try:

            repository = (
                SupportResistanceRepository(
                    db
                )
            )

            snapshot = SupportResistance(
                symbol=symbol,
                timeframe=timeframe,
                timestamp=datetime.now(
                    timezone.utc
                ),

                nearest_support=
                    analysis.get(
                        "nearest_support"
                    ),

                nearest_resistance=
                    analysis.get(
                        "nearest_resistance"
                    ),

                signal=
                    analysis.get(
                        "signal"
                    ),

                signal_level=
                    analysis.get(
                        "signal_level"
                    ),
            )

            return repository.save(
                snapshot
            )

        finally:
            db.close()