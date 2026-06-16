from database.session import SessionLocal

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from agents.candlestick_analysis_agent.agent import (
    CandlestickAnalysisAgent,
)

from services.candlestick_pattern_persistence_service import (
    CandlestickPatternPersistenceService,
)


def backfill(
    symbol: str = "RELIANCE",
    timeframe: str = "1d",
):

    db = SessionLocal()

    try:

        records = (
            OHLCVRepository(db)
            .get_history_by_symbol_and_timeframe(
                symbol,
                timeframe
            )
        )

        agent = (
            CandlestickAnalysisAgent()
        )

        created = 0

        for i in range(
            50,
            len(records)
        ):

            window = records[
                i - 50:i
            ]

            result = (
                agent.analyze(
                    list(
                        reversed(window)
                    )
                )
            )

            if result["patterns"]:

                CandlestickPatternPersistenceService.save_patterns(
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=window[-1].timestamp,
                    candlestick_score=result[
                        "candlestick_score"
                    ],
                    patterns=result[
                        "patterns"
                    ],
                )

                created += len(
                    result["patterns"]
                )

        print(
            "Patterns Created:",
            created
        )

    finally:
        db.close()


if __name__ == "__main__":
    backfill()