from agents.support_resistance_agent.agent import (
    SupportResistanceAgent,
)

from database.session import SessionLocal

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from utils.ohlcv_dataframe import (
    ohlcv_to_dataframe,
)

from utils.timeframe_validator import (
    validate_timeframe,
)


class SupportResistanceService:

    @staticmethod
    def analyze(
        symbol: str,
        timeframe: str = "1d"
    ):

        validate_timeframe(
            timeframe
        )

        db = SessionLocal()

        try:

            repository = OHLCVRepository(
                db
            )

            records = (
                repository
                .get_latest_by_symbol_and_timeframe(
                    symbol=symbol,
                    timeframe=timeframe,
                    limit=200
                )
            )

            if not records:
                return {
                    "supports": [],
                    "resistances": [],
                    "nearest_support": None,
                    "nearest_resistance": None,
                }

            data = ohlcv_to_dataframe(
                list(reversed(records))
            )

            agent = (
                SupportResistanceAgent()
            )

            return agent.analyze(
                data=data
            )

        finally:
            db.close()