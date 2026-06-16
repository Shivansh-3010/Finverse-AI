from database.session import SessionLocal

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from repositories.candlestick_pattern_repository import (
    CandlestickPatternRepository,
)


def test_alignment():

    db = SessionLocal()

    try:

        candles = (
            OHLCVRepository(db)
            .get_history_by_symbol_and_timeframe(
                "RELIANCE",
                "1d"
            )
        )

        patterns = (
            CandlestickPatternRepository(db)
            .get_history_by_timeframe(
                "RELIANCE",
                "1d"
            )
        )

        pattern_map = {
            p.timestamp: p
            for p in patterns
        }

        matched = 0

        for candle in candles:

            if candle.timestamp in pattern_map:
                matched += 1

        print(
            "OHLCV Records:",
            len(candles)
        )

        print(
            "Pattern Records:",
            len(patterns)
        )

        print(
            "Timestamp Matches:",
            matched
        )

    finally:
        db.close()


if __name__ == "__main__":
    test_alignment()