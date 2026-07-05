from database.session import SessionLocal

from repositories.ohlcv_repository import (
    OHLCVRepository,
)

from training.universe.universe_selector import (
    UniverseSelector,
)


def test_universe_size():

    db = SessionLocal()

    try:

        symbols = (
            UniverseSelector.get_symbols(
                db=db,
                timeframe="1d",
                min_candles=5000,
            )
        )

        repo = OHLCVRepository(db)

        total_rows = 0

        for symbol in symbols[:20]:

            rows = (
                repo.get_history_by_symbol_and_timeframe(
                    symbol,
                    "1d"
                )
            )

            total_rows += len(rows)

        avg_rows = total_rows / 20

        estimated_total = (
            avg_rows * len(symbols)
        )

        print(
            "\nAverage rows:",
            round(avg_rows)
        )

        print(
            "Estimated universe rows:",
            round(estimated_total)
        )

    finally:
        db.close()