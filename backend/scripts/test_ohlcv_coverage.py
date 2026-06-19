from database.session import SessionLocal

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

db = SessionLocal()

try:

    rows = (
        OHLCVRepository(db)
        .get_history_by_symbol_and_timeframe(
            "RELIANCE",
            "1d"
        )
    )

    print("Rows:", len(rows))

    print(
        "Earliest:",
        rows[0].timestamp.date()
    )

    print(
        "Latest:",
        rows[-1].timestamp.date()
    )

finally:
    db.close()