import pandas as pd

from agents.technical_analysis_agent.agent import TechnicalAnalysisAgent
from database.session import SessionLocal
from repositories.ohlcv_repository import OHLCVRepository
from utils.ohlcv_dataframe import ohlcv_to_dataframe
from feature_store.technical.technical_features import (
    generate_technical_features,
)

from services.indicator_persistence_service import (
    IndicatorPersistenceService,
)


class TechnicalAnalysisService:

        @staticmethod
        def analyze(symbol: str):

            db = SessionLocal()

            try:

                repository = OHLCVRepository(db)

                records = repository.get_latest_by_symbol(
                    symbol=symbol,
                    limit=200
                )

                if not records:
                    return {
                        "technical_score": 0,
                        "trend": "unknown",
                        "rsi": 0,
                        "reasons": ["No OHLCV data found"]
                    }

                data = ohlcv_to_dataframe(
                    list(reversed(records))
                )

                features = generate_technical_features(data)

                IndicatorPersistenceService.save_indicator(
                    symbol=symbol,
                    features=features
                )

                agent = TechnicalAnalysisAgent()

                return agent.analyze(data)

            finally:
                db.close()