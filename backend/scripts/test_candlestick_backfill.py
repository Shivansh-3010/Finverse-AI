from database.session import SessionLocal

from services.historical_candlestick_backfill_service import (
    HistoricalCandlestickBackfillService,
)


db = SessionLocal()

try:

    result = (
        HistoricalCandlestickBackfillService
        .backfill_symbol(
            db=db,
            symbol="RELIANCE",
            timeframe="1d",
        )
    )

    print(result)

finally:

    db.close()