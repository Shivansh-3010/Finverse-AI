from agents.candlestick_analysis_agent.agent import (
    CandlestickAnalysisAgent,
)
from services.candlestick_pattern_persistence_service import (
    CandlestickPatternPersistenceService,
)
from database.session import SessionLocal
from repositories.ohlcv_repository import OHLCVRepository


class CandlestickAnalysisService:

    @staticmethod
    def analyze(symbol: str):

        db = SessionLocal()

        try:

            repository = OHLCVRepository(db)

            records = repository.get_latest_by_symbol(
                symbol=symbol,
                limit=3
            )

            if not records:
                return {
                    "candlestick_score": 0,
                    "patterns": []
                }

            agent = CandlestickAnalysisAgent()

            result = agent.analyze(
                records
            )

            if result["patterns"]:

                CandlestickPatternPersistenceService.save_patterns(
                    symbol=symbol,
                    candlestick_score=
                        result["candlestick_score"],
                    patterns=result["patterns"],
                )

            return result

        finally:
            db.close()