import sqlite3
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from database.session import SessionLocal
from models.ohlcv_data import OHLCVData


SQLITE_DB_PATH = "../finverse.db"
BATCH_SIZE = 1000


def normalize_symbol(symbol: str) -> str:
    """
    Oracle -> PostgreSQL symbol normalization
    """
    if symbol.endswith(".NS"):
        return symbol[:-3]

    return symbol


def get_sqlite_connection():
    return sqlite3.connect(SQLITE_DB_PATH)


def get_symbol_timeframe_pairs(cursor):
    cursor.execute("""
        SELECT DISTINCT symbol, timeframe
        FROM ohlcv_data
        ORDER BY symbol, timeframe
    """)

    return cursor.fetchall()


def get_latest_pg_timestamp(
    db,
    symbol,
    timeframe
):
    return (
        db.query(
            func.max(OHLCVData.timestamp)
        )
        .filter(
            OHLCVData.symbol == symbol,
            OHLCVData.timeframe == timeframe
        )
        .scalar()
    )


def fetch_new_rows(
    cursor,
    oracle_symbol,
    timeframe,
    latest_pg_timestamp
):
    if latest_pg_timestamp is None:

        cursor.execute("""
            SELECT
                symbol,
                timeframe,
                timestamp,
                open,
                high,
                low,
                close,
                volume
            FROM ohlcv_data
            WHERE symbol = ?
            AND timeframe = ?
            ORDER BY timestamp
        """, (
            oracle_symbol,
            timeframe
        ))

    else:

        cursor.execute("""
            SELECT
                symbol,
                timeframe,
                timestamp,
                open,
                high,
                low,
                close,
                volume
            FROM ohlcv_data
            WHERE symbol = ?
            AND timeframe = ?
            AND timestamp > ?
            ORDER BY timestamp
        """, (
            oracle_symbol,
            timeframe,
            latest_pg_timestamp.isoformat()
        ))

    return cursor.fetchall()


def build_ohlcv_object(row):
    (
        symbol,
        timeframe,
        timestamp_str,
        open_price,
        high_price,
        low_price,
        close_price,
        volume
    ) = row

    return OHLCVData(
        symbol=normalize_symbol(symbol),
        timeframe=timeframe,
        timestamp=datetime.fromisoformat(timestamp_str),
        open=open_price,
        high=high_price,
        low=low_price,
        close=close_price,
        volume=volume,
        dividend=0,
        stock_split=0
    )


def bulk_insert(
    db,
    rows
):
    inserted = 0

    batch = []

    for row in rows:

        batch.append(
            build_ohlcv_object(row)
        )

        if len(batch) >= BATCH_SIZE:

            try:
                db.bulk_save_objects(batch)
                db.commit()
                inserted += len(batch)

            except IntegrityError:
                db.rollback()

            batch = []

    if batch:

        try:
            db.bulk_save_objects(batch)
            db.commit()
            inserted += len(batch)

        except IntegrityError:
            db.rollback()

    return inserted

def mark_rows_synced(
            cursor,
            oracle_symbol,
            timeframe
        ):
            cursor.execute("""
                UPDATE ohlcv_data
                SET synced = 1
                WHERE symbol = ?
                AND timeframe = ?
            """, (
                oracle_symbol,
                timeframe
            ))


def main():

    sqlite_conn = get_sqlite_connection()
    cursor = sqlite_conn.cursor()

    db = SessionLocal()

    total_inserted = 0
    processed_pairs = 0

    try:

        print("\n" + "=" * 80)
        print("ORACLE -> POSTGRESQL OHLCV SYNC")
        print("=" * 80)

        pairs = get_symbol_timeframe_pairs(
            cursor
        )

        for oracle_symbol, timeframe in pairs:

            try:

                pg_symbol = normalize_symbol(
                    oracle_symbol
                )

                latest_pg = (
                    get_latest_pg_timestamp(
                        db,
                        pg_symbol,
                        timeframe
                    )
                )

                rows = fetch_new_rows(
                    cursor,
                    oracle_symbol,
                    timeframe,
                    latest_pg
                )

                if not rows:
                    continue

                inserted = bulk_insert(
                    db,
                    rows
                )
                
                mark_rows_synced(
                    cursor,
                    oracle_symbol,
                    timeframe
                )

                sqlite_conn.commit()

                total_inserted += inserted
                processed_pairs += 1

                print(
                    f"{oracle_symbol:<20}"
                    f"{timeframe:<5}"
                    f" -> Inserted {inserted}"
                )

            except Exception as e:

                db.rollback()

                print(
                    f"ERROR: "
                    f"{oracle_symbol} "
                    f"{timeframe} "
                    f" -> {e}"
                )

        print("\n" + "=" * 80)
        print("SYNC COMPLETE")
        print("=" * 80)

        print(
            f"Pairs Processed : {processed_pairs}"
        )

        print(
            f"Rows Inserted   : {total_inserted}"
        )

    finally:

        db.close()
        sqlite_conn.close()


if __name__ == "__main__":
    main()  