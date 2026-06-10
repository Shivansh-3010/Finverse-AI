from datetime import datetime, timezone

from database.session import SessionLocal
from models.technical_indicator import TechnicalIndicator
from repositories.technical_indicator_repository import (
    TechnicalIndicatorRepository,
)


class IndicatorPersistenceService:

    @staticmethod
    def save_indicator(
        symbol: str,
        timeframe: str,
        features: dict
    ):

        db = SessionLocal()

        try:

            repository = TechnicalIndicatorRepository(db)

            indicator = TechnicalIndicator(
                symbol=symbol,
                timeframe=timeframe,
                timestamp=datetime.now(timezone.utc),

                rsi=features["rsi"],
                mfi=features["mfi"],

                sma_20=features["sma_20"],
                ema_20=features["ema_20"],

                macd=features["macd"],
                macd_signal=features["macd_signal"],

                adx=features["adx"],

                atr=features["atr"],

                obv=features["obv"],
                vwap=features["vwap"],

                bb_upper=features["bb_upper"],
                bb_middle=features["bb_middle"],
                bb_lower=features["bb_lower"],
            )

            return repository.save(indicator)

        finally:
            db.close()