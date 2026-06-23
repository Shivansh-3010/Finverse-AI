from database.session import SessionLocal
from sqlalchemy import text


def main():

    db = SessionLocal()

    try:

        result = db.execute(
            text("""
            DELETE FROM ohlcv_data
            WHERE close::text = 'NaN';
            """)
        )

        db.commit()

        print(
            f"Deleted rows: {result.rowcount}"
        )

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()