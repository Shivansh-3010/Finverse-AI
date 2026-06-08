from agents.candlestick_analysis_agent.agent import (
    CandlestickAnalysisAgent,
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

            return agent.analyze(
                records
            )

        finally:
            db.close()