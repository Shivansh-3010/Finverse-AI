from time import perf_counter

from database.session import SessionLocal

from models.ohlcv_data import OHLCVData
from models.technical_indicator import TechnicalIndicator
from models.candlestick_pattern import CandlestickPattern

from sqlalchemy import func


def benchmark(name, query_fn):

    start = perf_counter()

    result = query_fn()

    elapsed = perf_counter() - start

    print(
        f"{name:<40}"
        f"{elapsed:.4f}s"
    )

    return result


def main():

    db = SessionLocal()

    try:

        print("\n" + "=" * 80)
        print("ROW COUNTS")
        print("=" * 80)

        benchmark(
            "OHLCV Count",
            lambda: db.query(
                func.count(
                    OHLCVData.symbol
                )
            ).scalar()
        )

        benchmark(
            "Indicator Count",
            lambda: db.query(
                func.count(
                    TechnicalIndicator.symbol
                )
            ).scalar()
        )

        benchmark(
            "Candlestick Count",
            lambda: db.query(
                func.count(
                    CandlestickPattern.symbol
                )
            ).scalar()
        )

        print("\n" + "=" * 80)
        print("LATEST RECORD QUERIES")
        print("=" * 80)

        benchmark(
            "Latest OHLCV",
            lambda: (
                db.query(
                    OHLCVData
                )
                .filter(
                    OHLCVData.symbol == "RELIANCE"
                )
                .order_by(
                    OHLCVData.timestamp.desc()
                )
                .first()
            )
        )

        benchmark(
            "Latest Indicator",
            lambda: (
                db.query(
                    TechnicalIndicator
                )
                .filter(
                    TechnicalIndicator.symbol == "RELIANCE"
                )
                .order_by(
                    TechnicalIndicator.timestamp.desc()
                )
                .first()
            )
        )

        benchmark(
            "Latest Candlestick",
            lambda: (
                db.query(
                    CandlestickPattern
                )
                .filter(
                    CandlestickPattern.symbol == "RELIANCE",
                    CandlestickPattern.timeframe == "1d"
                )
                .order_by(
                    CandlestickPattern.timestamp.desc()
                )
                .first()
            )
        )

        print("\n" + "=" * 80)
        print("HISTORICAL QUERIES")
        print("=" * 80)

        benchmark(
            "1000 OHLCV Rows",
            lambda: (
                db.query(
                    OHLCVData
                )
                .filter(
                    OHLCVData.symbol == "RELIANCE"
                )
                .limit(1000)
                .all()
            )
        )

        benchmark(
            "1000 Indicator Rows",
            lambda: (
                db.query(
                    TechnicalIndicator
                )
                .filter(
                    TechnicalIndicator.symbol == "RELIANCE"
                )
                .limit(1000)
                .all()
            )
        )

        benchmark(
            "1000 Candlestick Rows",
            lambda: (
                db.query(
                    CandlestickPattern
                )
                .filter(
                    CandlestickPattern.symbol == "RELIANCE"
                )
                .limit(1000)
                .all()
            )
        )

        print("\n" + "=" * 80)
        print("DATABASE SCALE TEST COMPLETED")
        print("=" * 80)

    finally:

        db.close()


if __name__ == "__main__":
    main()