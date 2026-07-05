from database.session import SessionLocal

from repositories.candlestick_pattern_repository import (
    CandlestickPatternRepository,
)

from collections import Counter


def test_candlestick_duplicates():

    db = SessionLocal()

    try:

        patterns = (
            CandlestickPatternRepository(db)
            .get_history_by_timeframe(
                "RELIANCE",
                "1d"
            )
        )

        counts = Counter(
            p.timestamp
            for p in patterns
        )

        duplicated = [
            count
            for count in counts.values()
            if count > 1
        ]

        print(
            "\nTotal Pattern Rows:",
            len(patterns)
        )

        print(
            "Unique Timestamps:",
            len(counts)
        )

        print(
            "Duplicate Timestamps:",
            len(duplicated)
        )

        if duplicated:

            print(
                "Max Patterns Per Candle:",
                max(duplicated)
            )

            print(
                "Average Patterns Per Duplicate Candle:",
                round(
                    sum(duplicated)
                    / len(duplicated),
                    2
                )
            )

    finally:
        db.close()