from database.session import SessionLocal

from repositories.ohlcv_repository import (
    OHLCVRepository,
)


def test_history():

    db = SessionLocal()

    try:

        records = (
            OHLCVRepository(db)
            .get_history_by_symbol_and_timeframe(
                symbol="RELIANCE",
                timeframe="1d"
            )
        )

        print(
            "Record Count:",
            len(records)
        )

    finally:
        db.close()


if __name__ == "__main__":
    test_history()