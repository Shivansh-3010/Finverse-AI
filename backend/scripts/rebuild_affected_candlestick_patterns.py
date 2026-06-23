from database.session import SessionLocal

from services.historical_candlestick_backfill_service import (
    HistoricalCandlestickBackfillService,
)

AFFECTED_SYMBOLS = [
    'SBIN',
    'ASIANPAINT',
    'AXISBANK',
    'BPCL',
    'CIPLA',
    'DRREDDY',
    'GRASIM',
    'HDFC',
    'HDFCBANK',
    'HEROMOTOCO',
    'HINDALCO',
    'HINDUNILVR',
    'ICICIBANK',
    'INFY',
    'IOC',
    'ITC',
    'MM',
    'ONGC',
    'RELIANCE',
    'SUNPHARMA',
    'TATAMOTORS',
    'TATASTEEL',
    'TITAN',
    'WIPRO',
    'ZEEL',
    'BRITANNIA',
    'VEDL',
    'EICHERMOT',
    'HCLTECH',
    'BAJFINANCE',
    'GAIL',
    'KOTAKBANK',
    'INDUSINDBK',
    'SHREECEM',
    'BHARTIARTL',
    'MARUTI',
    'UPL',
    'LT',
    'ULTRACEMCO',
    'TCS',
    'NTPC',
    'JSWSTEEL',
    'TECHM',
    'POWERGRID',
    'ADANIPORTS',
    'BAJAJ-AUTO',
    'BAJAJFINSV',
    'NESTLEIND',
    'COALINDIA',
]


def main():

    db = SessionLocal()

    try:

        symbols = sorted(
            AFFECTED_SYMBOLS
        )

        print(
            f"Rebuilding {len(symbols)} affected symbols"
        )

        total_inserted = 0
        total_skipped = 0

        for symbol in symbols:

            print(
                "\n" + "=" * 80
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
            "\n" + "=" * 80
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