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
from services.candlestick_analysis_service import (
    CandlestickAnalysisService,
)

from technical.scoring.combined_score import (
    calculate_combined_score,
)

from utils.timeframe_validator import (
    validate_timeframe,
)


class TechnicalAnalysisService:

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

                repository = OHLCVRepository(db)

                records = repository.get_latest_by_symbol_and_timeframe(
                    symbol=symbol,
                    timeframe=timeframe,
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
                    timeframe=timeframe,
                    features=features
                )

                agent = TechnicalAnalysisAgent()

                technical_result = agent.analyze(data)

                candlestick_result = (
                    CandlestickAnalysisService.analyze(
                        symbol=symbol,
                        timeframe=timeframe
                    )
                )

                combined_score = calculate_combined_score(
                    technical_score=
                        technical_result["technical_score"],
                    candlestick_score=
                        candlestick_result["candlestick_score"],
                )

                technical_result["candlestick_score"] = (
                    candlestick_result["candlestick_score"]
                )

                technical_result["combined_score"] = (
                    combined_score
                )

                technical_result["candlestick_patterns"] = (
                    candlestick_result["patterns"]
                )

                return technical_result

            finally:
                db.close()