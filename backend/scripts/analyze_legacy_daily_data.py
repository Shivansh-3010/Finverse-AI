from database.session import SessionLocal
from sqlalchemy import text


def main():

    db = SessionLocal()

    try:

        result = db.execute(
            text("""
            SELECT
                symbol,
                COUNT(*) AS legacy_rows
            FROM ohlcv_data
            WHERE timeframe = '1d'
            AND timestamp::time = '00:00:00'
            GROUP BY symbol
            ORDER BY legacy_rows DESC;
            """)
        )

        total_rows = 0
        total_symbols = 0

        print("\nLEGACY DAILY DATA")
        print("=" * 80)

        for row in result:

            symbol = row[0]
            count = row[1]

            total_rows += count
            total_symbols += 1

            print(
                f"{symbol:<20} {count:,}"
            )

        print("\n" + "=" * 80)

        print(
            f"Symbols affected: {total_symbols:,}"
        )

        print(
            f"Rows to delete: {total_rows:,}"
        )

        print("=" * 80)

    finally:

        db.close()


if __name__ == "__main__":
    main()