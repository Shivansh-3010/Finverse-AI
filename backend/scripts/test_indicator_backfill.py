from database.session import SessionLocal

from services.historical_indicator_backfill_service import (
    HistoricalIndicatorBackfillService,
)

db = SessionLocal()

try:

    result = (
        HistoricalIndicatorBackfillService
        .backfill_symbol(
            db=db,
            symbol="RELIANCE",
            timeframe="1d",
        )
    )

    print(result)

finally:

    db.close()