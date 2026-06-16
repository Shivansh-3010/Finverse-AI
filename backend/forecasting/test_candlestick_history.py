from database.session import SessionLocal

from repositories.candlestick_pattern_repository import (
    CandlestickPatternRepository,
)


def test_history():

    db = SessionLocal()

    try:

        records = (
            CandlestickPatternRepository(db)
            .get_history_by_timeframe(
                symbol="RELIANCE",
                timeframe="1d"
            )
        )

        print(
            "Pattern Count:",
            len(records)
        )

        if records:
            print(
                "First:",
                records[0].timestamp
            )

            print(
                "Last:",
                records[-1].timestamp
            )

    finally:
        db.close()


if __name__ == "__main__":
    test_history()