from database.session import SessionLocal

from services.historical_candlestick_backfill_service import (
    HistoricalCandlestickBackfillService,
)


def main():

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


if __name__ == "__main__":
    main()