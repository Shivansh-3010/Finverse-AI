from database.session import SessionLocal
from sqlalchemy import text


def main():

    db = SessionLocal()

    try:

        print(
            "Deleting legacy daily candles..."
        )

        result = db.execute(
            text("""
            DELETE FROM ohlcv_data
            WHERE timeframe = '1d'
            AND timestamp::time = '00:00:00';
            """)
        )

        db.commit()

        print(
            f"Deleted rows: "
            f"{result.rowcount:,}"
        )

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()