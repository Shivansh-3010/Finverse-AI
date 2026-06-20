from database.session import SessionLocal

from models.ohlcv_data import OHLCVData

from services.historical_candlestick_backfill_service import (
    HistoricalCandlestickBackfillService,
)


def main():

    db = SessionLocal()

    try:

        symbols = (

            db.query(
                OHLCVData.symbol
            )

            .distinct()

            .all()
        )

        symbols = sorted(
            [
                row[0]
                for row in symbols
            ]
        )

        print(
            f"Found {len(symbols)} symbols"
        )

        total_inserted = 0
        total_skipped = 0

        for symbol in symbols:

            print(
                "\n"
                + "=" * 80
            )

            print(
                f"Processing {symbol}"
            )

            result = (
                HistoricalCandlestickBackfillService
                .backfill_symbol(
                    db=db,
                    symbol=symbol,
                    timeframe="1d",
                )
            )

            print(result)

            total_inserted += (
                result.get(
                    "inserted",
                    0,
                )
            )

            total_skipped += (
                result.get(
                    "skipped",
                    0,
                )
            )

        print(
            "\n"
            + "=" * 80
        )

        print(
            "TOTAL INSERTED:",
            f"{total_inserted:,}"
        )

        print(
            "TOTAL SKIPPED:",
            f"{total_skipped:,}"
        )

        print(
            "=" * 80
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()