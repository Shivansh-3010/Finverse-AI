from database.session import SessionLocal

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from utils.ohlcv_dataframe import (
    ohlcv_to_dataframe,
)


def test_close_distribution():

    db = SessionLocal()

    try:

        records = (
            OHLCVRepository(db)
            .get_history_by_symbol_and_timeframe(
                "RELIANCE",
                "1d",
            )
        )

        df = ohlcv_to_dataframe(records)

        next_close = df["close"].shift(-1)

        unchanged = (
            (df["close"] == next_close)
            .sum()
        )

        total = len(df)

        print(
            "\nRows:",
            total
        )

        print(
            "Unchanged Close:",
            unchanged
        )

        print(
            "Percent:",
            round(
                unchanged / total * 100,
                2
            ),
            "%"
        )

    finally:
        db.close()